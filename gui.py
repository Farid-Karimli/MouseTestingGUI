import tkinter as tk
from tkinter import *
import random
from timer import Timer
from fits import FitsLaw
import math

timer = Timer()
log = open("log.txt", "w+")

global fits
fits = None
selection_coordinates = []

window = tk.Tk()
window.title("Testing GUI")
width = 1000
height = 800

targets = 0

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def place_button_randomly():
    # Record click
    checkpoint = timer.checkpoint()
    log.write("Click " + str(checkpoint) + "\n")

    # Calculate Fits Law
    # print("Fits Law: " + str(fits.calculate_original_law(checkpoint)))
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

def remove_button(event):
    checkpoint = timer.checkpoint()
    print(checkpoint)
    global targets

    
    x,y = window.winfo_pointerx(), window.winfo_pointery()
    fits.to = event.widget.winfo_rootx(), event.widget.winfo_rooty()
    fits.select = x,y
    print(fits)
    fits.update()
    fits.f = x,y
    fits.times += [checkpoint]

    targets += 1

    if targets == 10:
        print("Fits modified:", fits.calculate_modified_law(timer.checkpoint()))
        event.widget.place_forget()
        return

    event.widget.place_forget()

# Places 10 buttons in a circle around the center of the screen
def place_directional_targets():

    top_left_corner = (width//2 , height//2 )
    print("top left corner: ", top_left_corner)
    # place button in top left corner
    button.place(x=top_left_corner[0], y=top_left_corner[1], anchor="center")
    
    newbutton = tk.Button(window, text="New", width=10, height=2, highlightbackground='red', bg='green', fg="black", font=("Arial", 20))

    # Places 3 buttons in a circle around the center of the screen 200 pixels away at 45 degree intervals
    arc = 0
    for i in range(3):
        arc += 45
        x = top_left_corner[0] + 200*math.cos(math.radians(arc))
        y = top_left_corner[1] + 200*math.sin(math.radians(arc))
        print("new x: ", x, "new y: ", y)

        newbutton = tk.Button(window, text="New", width=8, height=2, highlightbackground='red', bg='green', fg="black", font=("Arial", 20))
        newbutton.bind("<1>", remove_button)
        newbutton.place(x=x, y=y, anchor="center")


    
def place_simple_targets():

    for j in [2,4]:
        for i in range(1,10,2):
            target = tk.Button(window, text="Target", width=8, height=2, highlightbackground='gray', bg="gray", fg="black", font=("Arial", 15))
            target.place(x=100*i, y=100*j, anchor="center")
            target.bind("<1>", remove_button)


def increase_size():
    width = button.winfo_width()
    height = button.winfo_height()
    button.config(width=width+1, height=height+1)

def decrease_size():
    button.config(width=button.winfo_width()-1, height=button.winfo_height()-1)


def start_test():
    timer.start()
    start_button.place_forget()
    # Get cursor's current x and y coordinates
    x,y = window.winfo_pointerx(), window.winfo_pointery()
    dist = distance(x, y, width//2, 50)
    global fits
    fits = FitsLaw(8, dist)
    fits.f = (x,y)
    middle = (width//2 , height//2)
    #button.place(x=middle[0], y=middle[1], anchor="center")

    place_simple_targets()

def reset(event):
    print("Fits modified:", fits.calculate_modified_law(timer.checkpoint()))
    button.place_forget()
    start_button.place(x=width//2, y=height//2+75, anchor="center")



button = tk.Button(window, text="Target", width=8, height=2, highlightbackground='#3E4149', fg="white", font=("Arial", 15))

start_button = tk.Button(window, text="Start", width=10, height=2, highlightbackground='red', bg='red', fg="white", font=("Arial", 20),command=start_test)
start_button.place(x=width//2, y=height//2+75, anchor="center")

def mouseover(event):
    fits.to = button.winfo_rootx(), button.winfo_rooty()

def key(event):
    window.event_generate('<Motion>', warp=True, x=width//2, y=height//2)

window.bind('<space>', key)
# Bind the reset funtion to clicking q
window.bind('q', reset)

button.bind("<Enter>", mouseover)

window.geometry(f'{width}x{height}-5+40')
window.mainloop()

print(fits.calculate_modified_law(timer.checkpoint()))