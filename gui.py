import tkinter as tk
from tkinter.filedialog import asksaveasfile
import numpy as np
from tkinter import *
import random
from timer import Timer
from fits import FitsLaw
import math
import datetime

TODAY_DATE = datetime.datetime.today().strftime("%d-%m-%Y-%H-%M")

movement_log = open(f"movement_log_{TODAY_DATE}" + ".txt", "w")

# the arrangement is randomized, starting from the default position of 1
arrangement_start = 1

# LOGS
 
stats_log = open(f"stats_log_{TODAY_DATE}.csv", "w")
stats_log.write("Time, Click X, Click Y, Target X, Target Y, Target Number, Distance to TargetX, Distance to TargetY, Select X, Select Y, From X, From Y\n")

secondary_stats_log = open(f"secondary_stats_log_{TODAY_DATE}.txt", "w")

runs_log = open(f"runs_log_{TODAY_DATE}.csv", "w")
runs_log.write("Run, Throughput, Ballistic Time, Select Time, Number of TARGETS, Type of Arrangement\n")

# Create a dictionary of gestures and their corresponding numbers - UNUSED
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



# get screen size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# set window size to 80% of screen size
width = int(screen_width * 0.8)
height = int(screen_height * 0.7)


# UNUSED
TARGETS = 0
BLOCK = 0
TRIAL = 0
TRIALS = 5
BLOCKS = 3

buttons_dict = {}

def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def pause(event):
    print("Paused")
    timer.pause()
    timer2.pause()
    secondary_stats_log.write(f"Pause\n")
    stats_log.write(f"Pause\n")

    pause_button.config(text="Paused!")


def continue_timer(event):
    print("Continued")
    timer.continue_timer()
    timer2.continue_timer()
    continue_button.config(text="Continuing...")

def change_gesture():
    runs_log.write(f"Change Gesture\n")
    secondary_stats_log.write(f"Change Gesture\n")
    stats_log.write(f"Change Gesture\n")

    change_gesture_button.config(text="Changed!")

def remove_button(event, button_id):
    global TARGETS
    
    # Write click to movement log
    x,y = window.winfo_pointerx(), window.winfo_pointery()
    movement_log.write(
        f"Click at ({x}, {y}) target {TARGETS}. Time: {timer.get_elapsed()}\n")
    
    checkpoint = timer.stop()
    timer.start()
    print("checkpoint:", checkpoint)
    
    click_checkpoint = timer2.get_elapsed()
    timer2.start()
    fits.time_to_select += [click_checkpoint]
    
    secondary_stats_log.write(f"Select: {button_id}, {x}, {y}, {click_checkpoint}, {fits.f}\n")

    fits.to = event.widget.winfo_rootx(), event.widget.winfo_rooty()
    fits.select = x,y

    # write stats to stats log
    stats_log.write(  # Time, Click X, Click Y, Target X, Target Y, Target Number, Distance to TargetX, Distance to TargetY, Select X, Select Y, From X, From Y, Select time, Ballistic Time
        f"{checkpoint}, {x}, {y}, {event.widget.winfo_rootx()}, {event.widget.winfo_rooty()}, {button_id}, {fits.to[0]}, {fits.to[1]}, {fits.select[0]}, {fits.select[1]}, {fits.f[0]}, {fits.f[1]}\n")

    if button_id != 0:
        fits.update()
        fits.times += [checkpoint]

    fits.f = x,y
    
    TARGETS += 1

    if TARGETS == 10:
        global TRIAL
        TRIAL += 1
        event.widget.place_forget()
        reset(None, True)

    event.widget.place_forget()


def place_directional_targets():

    top_left_corner = (width//2 , height//2 )
    print("top left corner: ", top_left_corner)
    # place button in top left corner
    button.place(x=top_left_corner[0], y=top_left_corner[1], anchor="center")
    
    newbutton = tk.Button(window, text="New", width=10, height=2, highlightbackground='red', bg='green', fg="white", font=("Arial", 20))

    # Places 3 buttons in a circle around the center of the screen 200 pixels away at 45 degree intervals
    arc = 0
    for i in range(3):
        arc += 45
        x = top_left_corner[0] + 200*math.cos(math.radians(arc))
        y = top_left_corner[1] + 200*math.sin(math.radians(arc))
        print("new x: ", x, "new y: ", y)

        newbutton = tk.Button(window, text="New", width=8, height=2, highlightbackground='red', bg='green', fg="white", font=("Arial", 20))
        newbutton.bind("<1>", remove_button)
        newbutton.place(x=x, y=y, anchor="center")

def place_simple_targets():
    x = 0
    for j in [2,4]:
        for i in range(1,10,2):
            target = tk.Button(window, text=f"Target {x+1}", width=8, height=2, highlightbackground='gray', bg="gray", fg="white", font=("Arial", 15))
            buttons_dict[x] = target
            target.place(x=100*i, y=100*j, anchor="center")
            target.bind("<1>", remove_button)
            target.bind("<Enter>", mouseover)
            x+=1

def place_circle_targets(start):
    # Place 10 TARGETS in a circle around the center of the screen, where the first target is at the position start
    global buttons_dict

    addition = start - 1

    for i in range(10):
        if i == 0:
            number = 1
        elif i == 9:
            number = 10
        elif i == 5:
            number = 2
        else:
            number = prev_number + 2
        
        arc = (i+addition)*36
        x = width//2 + (width*0.25)*math.cos(math.radians(arc))
        y = height//2 + (height*0.4)*math.sin(math.radians(arc))
        print(x,y)

        target = tk.Button(window, text=f"{number}", width=3,  highlightbackground='black',
                           bg="black", fg="black", font=("Arial", 40), padx=0, pady=0, activebackground="gray", activeforeground="red", relief="raised")
        buttons_dict[number] = target
        # place the button so that it doesn't go off the screen
        target.place(x=x, y=y, anchor="center")
        window.update()
        #print(target.winfo_width(), target.winfo_height())
        target.bind("<1>", lambda event, id=number: remove_button(event, id))
        target.bind("<Enter>", lambda event, id=number: mouseover(event, id))

        prev_number = number

    #pause_button.place(x=100, y=50, anchor="center")
    # place a continue button next to the pause button
    #continue_button.place(x=200, y=50, anchor="center")

def increase_size():
    width = button.winfo_width()
    height = button.winfo_height()
    button.config(width=width+1, height=height+1)

def decrease_size():
    button.config(width=button.winfo_width()-1, height=button.winfo_height()-1)

def start_test():
    global TARGETS, arrangement_start
    TARGETS = 0

    # timer.start()
    # timer2.start()

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
    
    arrangement_start = random.randint(1,10)
    place_circle_targets(arrangement_start)

def reset(event, remove_buttons=False):
        global throughputs, ballistics, selects, gestures, TRIAL, BLOCK, buttons_dict, TARGETS, arrangement_start

        if remove_buttons:
            print("removing buttons")
            for button in buttons_dict:
                buttons_dict[button].place_forget()
            buttons_dict.clear()
            
        else:     
            buttons_dict[button].place_forget()
        start_button.place(x=width//2, y=height//2+75, anchor="center")

        """Show how many TRIALs left in this BLOCK
        instructions.config(text=f"TRIAL {TRIAL} of {TRIALS} for this gesture")
        instructions.place(x=width//2, y=height//2-75, anchor="center")"""

    
        stats = fits.get_average_times()
        throughput = fits.calculate_modified_law(timer.stop())
        timer.start()

        current_gesture = "Gesture " + str(BLOCK+1)
        throughputs[current_gesture] += [throughput]
        ballistics[current_gesture] += [stats[0]]
        selects[current_gesture] += [stats[1]]

        # Write to runs log
        runs_log.write(f"{TRIAL+1}, {throughput}, {stats[0]}, {stats[1]}, {TARGETS}, {arrangement_start}\n")

        
        ''' if TRIAL == TRIALS: 
                TRIAL = 0
                BLOCK += 1
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


            

        """if BLOCK == BLOCKS: # Finished all BLOCKs
            finished_label = tk.Label(window, text="Test Complete", font=("Helvetica", 18))
            finished_label.place(x=width//2, y=height//2-150, anchor="center")

            gesture_label.place_forget()

            results_file = asksaveasfile(mode='w', defaultextension=".csv")
    
            with results_file as f:
                f.write("Gesture, Throughput, Ballistic Time, Select Time\n")
                for BLOCK in range(BLOCKS):
                    gesture_name = "Gesture " + str(BLOCK+1)
                    f.write(f"{gesture_name}, {round(np.mean(throughputs[gesture_name]),2)}, {round(np.mean(ballistics[gesture_name]),2)}, {round(np.mean(selects[gesture_name]),2)}\n")
                  """
                  
button = tk.Button(window, text="Target", width=8, height=2, highlightbackground='#3E4149', fg="white", font=("Arial", 15))

start_button = tk.Button(window, text="Start", width=10, height=2, highlightbackground='red', bg='red', fg="white", font=("Arial", 20),command=start_test)
start_button.place(x=width//2, y=height//2+75, anchor="center")

pause_button = tk.Button(window, text="Pause", width=8, height=2, highlightbackground='red', bg='blue', fg="white", font=("Arial", 15))
pause_button.bind("<1>", pause)
pause_button.bind("p", pause)

continue_button = tk.Button(window, text="Continue", width=8, height=2, highlightbackground='red', bg='green', fg="white", font=("Arial", 15))
continue_button.bind("<1>", continue_timer)
continue_button.bind('c', continue_timer)

#Create label
instructions = tk.Label(window, text="Click the start button below to start", font=("Helvetica", 18))
instructions.place(x=width//2, y=height//2-75, anchor="center")

throughput_label = tk.Label(window, font=("Helvetica", 22))
ballistic_time_label = tk.Label(window, font=("Helvetica", 18))
select_time_label    = tk.Label(window, font=("Helvetica", 18))

change_gesture_button = tk.Button(window, text="Change Gesture", width=20, height=2, highlightbackground='red', bg='pink', fg="black", font=("Arial", 20), command=change_gesture)
change_gesture_button.place(x=width//2, y=height//2+170, anchor="center")

# button to reset in the top right corner
reset_button = tk.Button(window, text="Reset", width=8, height=2, highlightbackground='red', bg='red', fg="black", font=("Arial", 20), command=lambda : reset(None, True))
reset_button.place(x=width-20, y=0, anchor="ne")

def mouseover(event, button_id):
    enter_checkpoint = timer2.stop()
    timer2.start()
    fits.ballistic_times += [enter_checkpoint]
    # get x and y coordinates of event
    x,y = event.x, event.y
    # write to stats2 log the button that was clicked and the x and y coordinates of the mouse and the ballistics time
    secondary_stats_log.write(f"Ballistic: {button_id}, {x}, {y}, {enter_checkpoint}\n")
    
def key(event):
    window.event_generate('<Motion>', warp=True, x=width//2, y=height//2)


def motion(event):
    x, y = event.x, event.y
    movement_log.write(f"{x}, {y}\n")

window.bind('<Motion>', motion)
window.bind('<space>', key)
button.bind("<Enter>", mouseover)

window.geometry(f'{width}x{height}')
window.mainloop()
stats_log.close()
runs_log.close()
movement_log.close()
