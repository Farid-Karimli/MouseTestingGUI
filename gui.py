import tkinter as tk
from tkinter.filedialog import asksaveasfile
import numpy as np
from tkinter import *
import random
from timer import Timer
from fits import FitsLaw
import math

movement_log = open("movement_log.txt", "w")

stats_log = open("stats_log.csv", "w")
stats_log.write("Time, Click X, Click Y, Target X, Target Y, Target Number, Distance to TargetX, Distance to TargetY, Select X, Select Y, From X, From Y\n")

stats2_log = open("stats2_log.txt", "w")

runs_log = open("runs_log.csv", "w")
runs_log.write("Run, Throughput, Ballistic Time, Select Time\n")

# Create a dictionary of gestures and their corresponding numbers
throughputs = {"Gesture 1": [],  "Gesture 2": [], "Gesture 3": []}
ballistics = {"Gesture 1": [], "Gesture 2": [], "Gesture 3": []}
selects = {"Gesture 1": [],  "Gesture 2": [], "Gesture 3": []}

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
block = 0
trial = 0

TRIALS = 5
BLOCKS = 3

buttons_d = {}

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def pause(event):
    print("Paused")
    timer.pause()
    timer2.pause()
    stats2_log.write(f"Pause\n")
    stats_log.write(f"Pause\n")

def continue_timer(event):
    print("Continued")
    timer.continue_timer()
    timer2.continue_timer()

def change_gesture():
    runs_log.write(f"Change Gesture\n")
    stats2_log.write(f"Change Gesture\n")
    stats_log.write(f"Change Gesture\n")


def remove_button(event, button_id):
    global targets

    print("This is the button id: ", button_id)
    '''if buttons_d[targets] != event.widget: # Can't click on this button
        return'''
    
    # Write click to movement log
    x,y = window.winfo_pointerx(), window.winfo_pointery()
    movement_log.write(
        f"Click at ({x}, {y}) target {targets}. Time: {timer.get_elapsed()}\n")

    checkpoint = timer.stop()
    timer.start()
    print("checkpoint:", checkpoint)
    
    click_checkpoint = timer2.get_elapsed()
    timer2.start()
    #print(click_checkpoint)
    fits.time_to_select += [click_checkpoint]
    
    
    stats2_log.write(f"Select: {button_id}, {x}, {y}, {click_checkpoint}, {fits.f}\n")

    fits.to = event.widget.winfo_rootx(), event.widget.winfo_rooty()
    fits.select = x,y

    # write stats to stats log
    stats_log.write(  # Time, Click X, Click Y, Target X, Target Y, Target Number, Distance to TargetX, Distance to TargetY, Select X, Select Y, From X, From Y, Select time, Ballistic Time
        f"{checkpoint}, {x}, {y}, {event.widget.winfo_rootx()}, {event.widget.winfo_rooty()}, {button_id}, {fits.to[0]}, {fits.to[1]}, {fits.select[0]}, {fits.select[1]}, {fits.f[0]}, {fits.f[1]}\n")


    fits.update()
    fits.f = x,y
    fits.times += [checkpoint]

    targets += 1

    if targets == 10:
        global trial
        trial += 1
        event.widget.place_forget()
        reset(None, True)


    event.widget.place_forget()

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
    x = 0
    for j in [2,4]:
        for i in range(1,10,2):
            target = tk.Button(window, text=f"Target {x+1}", width=8, height=2, highlightbackground='gray', bg="gray", fg="black", font=("Arial", 15))
            buttons_d[x] = target
            target.place(x=100*i, y=100*j, anchor="center")
            target.bind("<1>", remove_button)
            target.bind("<Enter>", mouseover)
            x+=1

def place_circle_targets():
    # Place 10 targets in a circle around the center of the screen

    for i in range(10):
        arc = i*36
        x = width//2 + 350*math.cos(math.radians(arc))
        y = height//2 + 350*math.sin(math.radians(arc))

        target = tk.Button(window, text=f"Target {i+1}", width=8, height=2, highlightbackground='gray', bg="gray", fg="black", font=("Arial", 15))
        buttons_d[i] = target
        target.place(x=x, y=y, anchor="center")
        target.bind("<1>", lambda event, id=i: remove_button(event, id))
        target.bind("<Enter>", lambda event, id=i: mouseover(event, id))


    # place a pause button in the top left of the screen
    pause_button = tk.Button(window, text="Pause", width=8, height=2, highlightbackground='red', bg='blue', fg="white", font=("Arial", 15))
    pause_button.place(x=100, y=50, anchor="center")

    pause_button.bind("<1>", pause)

    # place a continue button next to the pause button
    continue_button = tk.Button(window, text="Continue", width=8, height=2, highlightbackground='red', bg='green', fg="white", font=("Arial", 15))
    continue_button.place(x=200, y=50, anchor="center")

    continue_button.bind("<1>", continue_timer)

    
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
    change_gesture_button.place_forget()


    # Get cursor's current x and y coordinates
    x,y = window.winfo_pointerx(), window.winfo_pointery()
    dist = distance(x, y, width//2, 50)
    global fits
    fits = FitsLaw(8, dist)
    fits.f = (x,y)
    
    place_circle_targets()

def reset(event, show_stats=False):
        global throughputs, ballistics, selects, gestures, trial, block

        button.place_forget()
        start_button.place(x=width//2, y=height//2+75, anchor="center")

        """Show how many trials left in this block
        instructions.config(text=f"Trial {trial} of {TRIALS} for this gesture")
        instructions.place(x=width//2, y=height//2-75, anchor="center")"""

    
        stats = fits.get_average_times()
        throughput = fits.calculate_modified_law(timer.stop())
        timer.start()

        current_gesture = "Gesture " + str(block+1)
        throughputs[current_gesture] += [throughput]
        ballistics[current_gesture] += [stats[0]]
        selects[current_gesture] += [stats[1]]

        # Write to runs log
        runs_log.write(f"{trial+1}, {throughput}, {stats[0]}, {stats[1]}\n")

        
        ''' if trial == TRIALS: 
                trial = 0
                block += 1
        '''

        average_throughput = np.mean(throughputs[current_gesture])
        average_ballistic = np.mean(ballistics[current_gesture])
        average_select = np.mean(selects[current_gesture])
        print(average_throughput, average_ballistic, average_select)

        throughput_label.config(text=f"Throughput: {round(average_throughput,2)}")
        ballistic_time_label.config(text=f"Average time to get to target: {round(average_ballistic,2)} s")
        select_time_label.config(text=f"Average time to select target: {round(average_select,2)} s")

        throughput_label.place(x=width//2, y=height//2-145, anchor="center")
        ballistic_time_label.place(x=width//2, y=height//2-100, anchor="center")
        select_time_label.place(x=width//2, y=height//2-60, anchor="center")

        change_gesture_button.config(text=f"Change gesture")
        change_gesture_button.place(
            x=width//2, y=height//2+150, anchor="center")


            

        """if block == BLOCKS: # Finished all blocks
            finished_label = tk.Label(window, text="Test Complete", font=("Helvetica", 18))
            finished_label.place(x=width//2, y=height//2-150, anchor="center")

            gesture_label.place_forget()

            results_file = asksaveasfile(mode='w', defaultextension=".csv")
    
            with results_file as f:
                f.write("Gesture, Throughput, Ballistic Time, Select Time\n")
                for block in range(BLOCKS):
                    gesture_name = "Gesture " + str(block+1)
                    f.write(f"{gesture_name}, {round(np.mean(throughputs[gesture_name]),2)}, {round(np.mean(ballistics[gesture_name]),2)}, {round(np.mean(selects[gesture_name]),2)}\n")
                  """
                  
                  

button = tk.Button(window, text="Target", width=8, height=2, highlightbackground='#3E4149', fg="white", font=("Arial", 15))

start_button = tk.Button(window, text="Start", width=10, height=2, highlightbackground='red', bg='red', fg="white", font=("Arial", 20),command=start_test)
start_button.place(x=width//2, y=height//2+75, anchor="center")

#Create label
instructions = tk.Label(window, text="Click the start button below to start", font=("Helvetica", 18))
instructions.place(x=width//2, y=height//2-75, anchor="center")

throughput_label = tk.Label(window, font=("Helvetica", 22))
ballistic_time_label = tk.Label(window, font=("Helvetica", 18))
select_time_label    = tk.Label(window, font=("Helvetica", 18))

change_gesture_button = tk.Button(window, text="Change Gesture", width=20, height=2, highlightbackground='red', bg='pink', fg="black", font=("Arial", 20), command=change_gesture)
change_gesture_button.place(x=width//2, y=height//2+170, anchor="center")

def mouseover(event, button_id):
    if event.widget == buttons_d[targets]:
        enter_checkpoint = timer2.stop()
        timer2.start()
        fits.ballistic_times += [enter_checkpoint]
        # get x and y coordinates of event
        x,y = event.x, event.y
        # write to stats2 log the button that was clicked and the x and y coordinates of the mouse and the ballistics time
        stats2_log.write(f"Ballistic: {button_id}, {x}, {y}, {enter_checkpoint}\n")
        


def key(event):
    window.event_generate('<Motion>', warp=True, x=width//2, y=height//2)


def motion(event):
    x, y = event.x, event.y
    movement_log.write(f"{x}, {y}\n")

window.bind('<Motion>', motion)

window.bind('<space>', key)
# Bind the reset funtion to clicking q
# window.bind('q', reset)

button.bind("<Enter>", mouseover)

window.geometry(f'{width}x{height}-5+40')
window.mainloop()
stats_log.close()
runs_log.close()
movement_log.close()
