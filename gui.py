import tkinter as tk
import numpy as np
from tkinter import *
import random
from timer import Timer
from fits import FitsLaw
import math

# gesture_order = "E M O D D O E M M E M E O M E O O D D D".split()
gesture_order = "M M E E".split(" ")
gestures = {"E": "Eyebrow Raise", "O": "Mouth Open", "D": "Dwell Time", "M": "Mouse"}
gesture_index = 0

timer = Timer()
timer2 = Timer()    

global fits
fits = None
selection_coordinates = []

window = tk.Tk()
window.title("Testing GUI")
width = 1000
height = 800

targets = 0

TRIALS = 5
throughputs = {"Dwell Time": [], "Mouse": [], "Eyebrow Raise": [], "Mouth Open": []}
ballistics = {"Dwell Time": [], "Mouse": [], "Eyebrow Raise": [], "Mouth Open": []}
selects = {"Dwell Time": [], "Mouse": [], "Eyebrow Raise": [], "Mouth Open": []}


def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def place_button_randomly():
    # Record click
    checkpoint = timer.checkpoint()

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
    global targets
    
    checkpoint = timer.checkpoint()
    #print(checkpoint)
    
    click_checkpoint = timer2.checkpoint()
    #print(click_checkpoint)
    fits.time_to_select += [click_checkpoint]
    
    x,y = window.winfo_pointerx(), window.winfo_pointery()
    fits.to = event.widget.winfo_rootx(), event.widget.winfo_rooty()
    fits.select = x,y
    #print(fits)
    fits.update()
    fits.f = x,y
    fits.times += [checkpoint]

    targets += 1

    if targets == 10:
        event.widget.place_forget()
        reset(None, True)


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
            target.bind("<Enter>", mouseover)



def increase_size():
    width = button.winfo_width()
    height = button.winfo_height()
    button.config(width=width+1, height=height+1)

def decrease_size():
    button.config(width=button.winfo_width()-1, height=button.winfo_height()-1)

def start_test():
    global targets
    targets = 0

    timer.start()
    timer2.start()

    throughput_label.place_forget()
    ballistic_time_label.place_forget()
    select_time_label.place_forget()
    start_button.place_forget()
    instructions.place_forget()
    gesture_label.place_forget()

    # Get cursor's current x and y coordinates
    x,y = window.winfo_pointerx(), window.winfo_pointery()
    dist = distance(x, y, width//2, 50)
    global fits
    fits = FitsLaw(8, dist)
    fits.f = (x,y)
    
    place_simple_targets()

def reset(event, show_stats=False):
    # print("Fits modified:", fits.calculate_modified_law(timer.checkpoint()))
    
    button.place_forget()
    start_button.place(x=width//2, y=height//2+75, anchor="center")

    if show_stats:
        stats = fits.get_average_times()
        throughput = fits.calculate_modified_law(timer.checkpoint())

        global throughputs, ballistics, selects, gestures, gesture_order, gesture_index
        current_gesture = gestures[gesture_order[gesture_index]]
        throughputs[current_gesture] += [throughput]
        ballistics[current_gesture] += [stats[0]]
        selects[current_gesture] += [stats[1]]

        '''throughput_label.config(text=f"Throughput: {round(throughput,2)}")
        ballistic_time_label.config(text=f"Average time to get to target: {round(stats[0],2)}ms")
        select_time_label.config(text=f"Average time to select target: {round(stats[1],2)}ms")

        throughput_label.place(x=width//2, y=height//2-110, anchor="center")
        ballistic_time_label.place(x=width//2, y=height//2-75, anchor="center")
        select_time_label.place(x=width//2, y=height//2-50, anchor="center")
        '''
        gesture_index += 1

        if gesture_index == len(gesture_order):
            print("Finished all gestures")
            # Create a file and write the averages to it
            with open("results.txt", "w") as f:
                f.write("Gesture, Throughput, Ballistic Time, Select Time\n")
                for gesture in gestures:
                    gesture_name = gestures[gesture]
                    f.write(f"{gesture}, {round(np.mean(throughputs[gesture_name]),2)}, {round(np.mean(ballistics[gesture_name]),2)}, {round(np.mean(selects[gesture_name]),2)}\n")
            
        else:
            gesture_label.config(text="Gesture: " + gestures[gesture_order[gesture_index]])
            gesture_label.place(x=width//2, y=height//2-150, anchor="center")



button = tk.Button(window, text="Target", width=8, height=2, highlightbackground='#3E4149', fg="white", font=("Arial", 15))

start_button = tk.Button(window, text="Start", width=10, height=2, highlightbackground='red', bg='red', fg="white", font=("Arial", 20),command=start_test)
start_button.place(x=width//2, y=height//2+75, anchor="center")

#Create label
instructions = tk.Label(window, text="Click the start button below to start", font=("Helvetica", 18))
instructions.place(x=width//2, y=height//2-75, anchor="center")

throughput_label = tk.Label(window, font=("Helvetica", 22))
ballistic_time_label = tk.Label(window, font=("Helvetica", 18))
select_time_label    = tk.Label(window, font=("Helvetica", 18))

gesture_label = tk.Label(window, text="Gesture: " + gestures[gesture_order[gesture_index]], font=("Helvetica", 18))
gesture_label.place(x=width//2, y=height//2-150, anchor="center")

def mouseover(event):
    enter_checkpoint = timer2.checkpoint()
    #print(enter_checkpoint)
    fits.ballistic_times += [enter_checkpoint]


def key(event):
    window.event_generate('<Motion>', warp=True, x=width//2, y=height//2)

window.bind('<space>', key)
# Bind the reset funtion to clicking q
# window.bind('q', reset)

button.bind("<Enter>", mouseover)

window.geometry(f'{width}x{height}-5+40')
window.mainloop()
