from itertools import *
from random import *
from tkinter import *
from tkinter import messagebox
import pygame, sys
from pygame.locals import *
import time
canvas_width=800
canvas_height=400

win= Tk()

pygame.mixer.init()
pygame.mixer_music.load("Background.mp3")
pygame.mixer.music.set_volume(0.05)
pygame.mixer_music.play(-1,0.0)


level=input("Enter level : easy, medium, hard\n") #difficulty level
if level=="easy":
    difficulty_factor=1
elif level=="medium":
    difficulty_factor=0.9
else:
    difficulty_factor=0.7

c=Canvas(width=canvas_width,height=canvas_height,background='skyblue')
c.create_rectangle(0,canvas_height-80,canvas_width,canvas_height,fill='green')
c.pack()
bowl_color='black'
bowl_width=100
bowl_height=100
bowl_start_x=canvas_width/2 - bowl_width/2
bowl_start_y=canvas_height - bowl_height - 20
bowl_start_x2=bowl_start_x+bowl_width
bowl_start_y2=bowl_start_y+bowl_height
bowl=c.create_arc(bowl_start_x,bowl_start_y,bowl_start_x2,bowl_start_y2, start=200,extent=140,style='arc',outline=bowl_color,width=3)
# egg creation
egg_width=40
egg_height=60
egg_score=10
egg_speed=500
egg_interval=4000
# difficulty_factor=1
eggs=[]
color_cycle = cycle(['red' , 'yellow' , 'pink' , 'white' , 'black'])

score=0
lives=3
score_text=c.create_text(10,10,anchor='nw',font=('Arial',20,'bold'),fill='blue',text='score-'+str(score))
lives_text=c.create_text(canvas_width-10,10,anchor='ne',font=('Arial',20,'bold'),fill='blue',text='lives-'+str(lives))

def create_eggs():
    x=randrange(10,750)
    y=40
    new_egg=c.create_oval(x,y,x+egg_width,y+egg_height,fill=next(color_cycle),width=0)
    eggs.append(new_egg)
    win.after(egg_interval,create_eggs)
   
def move_eggs():
    for egg in eggs:
        (egg_x,egg_y,egg_x2,egg_y2) = c.coords(egg)
        c.move(egg,0,10)
        print(canvas_height, egg_y2)
        if egg_y2 > canvas_height:
            eggDropped(egg)
    win.after(egg_speed,move_eggs)

def eggDropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    reduceLife()
    if(lives==0):
        win.after(2000,win.destroy)
        messagebox.showinfo('GAME OVER!!!','Final-Score - '+str(score))
        

def reduceLife():
    global lives
    lives-=1
    c.itemconfigure(lives_text,text='lives-'+str(lives))

def bowlCatch_check():
    (bowl_x,bowl_y,bowl_x2,bowl_y2)=c.coords(bowl)
    for egg in eggs:
        (egg_x,egg_y,egg_x2,egg_y2)=c.coords(egg)
        if bowl_x < egg_x and egg_x2 < bowl_x2 and bowl_y2-egg_y2<40:
            eggs.remove(egg)
            c.delete(egg)
            increaseScore(egg_score)
    win.after(100,bowlCatch_check)

def increaseScore(s):
    global score,egg_speed,egg_interval
    score+=s
    egg_speed=int(egg_speed*difficulty_factor)
    egg_interval=int(egg_interval*difficulty_factor)
    c.itemconfigure(score_text,text='score-'+str(score))


def moveBowl_left(event):
    (x1,y1,x2,y2)=c.coords(bowl)
    if x1>0:
        c.move(bowl,-20,0)

def moveBowl_right(event):
    (x1,y1,x2,y2)=c.coords(bowl)
    if x2<canvas_width:
         c.move(bowl,20,0)


c.bind('<Left>', moveBowl_left)
c.bind('<Right>', moveBowl_right)
c.focus_set()


win.after(1000,create_eggs)
win.after(1000,move_eggs)
win.after(1000,bowlCatch_check)
win.mainloop()