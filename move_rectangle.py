# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 17:51:36 2018

@author: jess
"""

from tkinter import *
import speech_recognition as sr
from gtts import gTTS
import os
import time
from random import randint


def get_audio():
    direction = ''
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # here
        print("Dites quelque chose")
        audio = r.listen(source,timeout=3)
    
    # recognize speech using Google
    try:
        print("Vous avez dit " + r.recognize_google(audio))
        direction = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google could not understand audio")
    except sr.RequestError as e:
        print("Google error; {0}".format(e))
        
    if direction != '':
        if 'gauche' in direction:
            direction = 'left'
        if 'droite' in direction:
            direction = 'right'
        if 'haut' in direction:
            direction = 'up'
        if 'bas' in direction:
            direction = 'down'
        return direction
        
def pain():
    lines = ["oh","aïe","pourquoi vous me faites mal?","ca fait mal","quelle douleur horrible","je ne merite pas tout ca"]
    tmp = randint(0,len(lines)-1)
    return lines[tmp]
    

class Rectangle(Frame):
    
    def __init__(self):
        Frame.__init__(self, bg = "white")
        self.master.title("Rectangle")
        self.grid()
        self.radius = 50 
        self.canvas = Canvas(self, width = 400, height = 400, bg = "white")
        self.canvas.grid(row = 0, column = 0)
        self.canvas.create_rectangle(10,10,100,100, outline="#fb0", fill="#fb0", tags = "Rectangle")
        self.canvas.create_text(200, 200, text = "", tags = "text")
        self.canvas.bind('<Up>', self.moveRectangle)
        self.canvas.bind('<Down>', self.moveRectangle)
        self.canvas.bind('<Left>', self.moveRectangle)
        self.canvas.bind('<Right>', self.moveRectangle)
        self.canvas.bind('<space>', self.moveRectangle)
        self.canvas.focus_set()
        
    def moveRectangle(self, event):
        """move Rectangle up, down, left or right when user clicks an arrow key"""
        x=0
        y=0
        direct = ""
        if event.keysym == "space":
            direct = get_audio()
        if direct == 'up' or event.keysym == "Up":
            y = -10
        elif direct == "down" or event.keysym == "Down":
            y = 10
        elif direct == "left" or event.keysym == "Left":
            x = -10
        elif direct == "right" or event.keysym == "Right":
            x = 10
            
        #move rectangle    
        self.canvas.move("Rectangle", x, y)
        self.canvas.update()
        coords = self.canvas.coords("Rectangle")
        
        #check no crashes
        if any(i >= 400 for i in coords) or any(i <= 0 for i in coords):
            txt = pain()
            tts = gTTS(text = txt +'!', lang='fr')
            txt = txt.replace(' ','_')
            tts.save(txt + ".mp3")
            os.system("play "+ txt +".mp3")
            if direct == 'up' or event.keysym == "Up":
                y = 10
            elif direct == "down" or event.keysym == "Down":
                y = -10
            elif direct == "left" or event.keysym == "Left":
                x = 10
            elif direct == "right" or event.keysym == "Right":
                x = -10
                
            #move rectangle    
            self.canvas.move("Rectangle", x, y)
            self.canvas.update()
            coords = self.canvas.coords("Rectangle")
        print(coords)
        
def main():
    Rectangle().mainloop()
    
print("Press space to talk")
main()