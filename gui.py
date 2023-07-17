import tkinter as tk
from tkinter import *
import random
from timer import Timer
from fits import FitsLaw

timer = Timer()
log = open("log.txt", "w+")

global fits
fits = None
selection_coordinates = []

window = tk.Tk()
window.title("Testing GUI")
width = 700
height = 590


def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def place_button_randomly():
    # Record click
    checkpoint = timer.checkpoint()
    log.write("Click " + str(checkpoint) + "\n")

    # Calculate Fits Law
    print("Fits Law: " + str(fits.calculate_original_law(checkpoint)))
    x,y = window.winfo_pointerx(), window.winfo_pointery()
    fits.select = x,y
    #print it
    fits.update()
    # Get button's current x and y coordinates
    x,y = button.winfo_rootx(), button.winfo_rooty()
    try: 
        random_x = random.randint(x-100 if x-100 > 0 else width//4, x+100 if x+110 < width else width - width//4)
        random_y = random.randint(y-100 if y-100 > 0 else height//4, y+100 if y+102 < height else height - height//4)
    except ValueError:
        random_x = random.randint(width//4, width - width//4)
        random_y = random.randint(height//4, height - height//4)

    fits.target_width = 8
    fits.distance_to_target = distance(x, y, random_x, random_y)
    fits.f = x,y 

    button.place(x=random_x, y=random_y, anchor="center")

def increase_size():
    width = button.winfo_width()
    height = button.winfo_height()
    button.config(width=width+1, height=height+1)

def decrease_size():
    button.config(width=button.winfo_width()-1, height=button.winfo_height()-1)


def start_test():
    timer.start()
    start_button.place_forget()
    button.place(x=width//2, y=50, anchor="center")
    # Get cursor's current x and y coordinates
    x,y = window.winfo_pointerx(), window.winfo_pointery()
    dist = distance(x, y, width//2, 50)
    global fits
    fits = FitsLaw(8, dist)
    fits.f = (x,y)

def reset(event):
    print("Fits modified:", fits.calculate_modified_law(timer.checkpoint()))
    button.place_forget()
    start_button.place(x=width//2, y=height//2+75, anchor="center")



button = tk.Button(window, text="Target", width=8, height=2, highlightbackground='#3E4149', fg="white", font=("Arial", 15),command=place_button_randomly)

start_button = tk.Button(window, text="Start", width=10, height=2, highlightbackground='red', bg='red', fg="white", font=("Arial", 20),command=start_test)
start_button.place(x=width//2, y=height//2+75, anchor="center")

def mouseover(event):
    checkpoint = timer.checkpoint()
    fits.to = button.winfo_rootx(), button.winfo_rooty()
    # print it 
    log.write("Mouseover " + str(checkpoint) + "\n")

def key(event):
    window.event_generate('<Motion>', warp=True, x=width//2, y=height//2)

window.bind('<space>', key)
# Bind the reset funtion to clicking q
window.bind('q', reset)

button.bind("<Enter>", mouseover)

window.geometry(f'{width}x{height}-5+40')
window.mainloop()

