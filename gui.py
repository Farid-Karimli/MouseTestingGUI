import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
import random
from timer import Timer

timer = Timer()
log = open("log.txt", "w+")


window = tk.Tk()
window.title("Testing GUI")
width = 700
height = 590

def place_button_randomly():
    # Record click
    log.write("Click " + str(timer.checkpoint()) + "\n")

    # Get button's current x and y coordinates
    x,y = button.winfo_rootx(), button.winfo_rooty()
    try: 
        random_x = random.randint(x-100 if x-100 > 0 else width//4, x+100 if x+110 < width else width - width//4)
        random_y = random.randint(y-100 if y-100 > 0 else height//4, y+100 if y+102 < height else height - height//4)
    except ValueError:
        random_x = random.randint(width//4, width - width//4)
        random_y = random.randint(height//4, height - height//4)

    # print(random_x, random_y)

    button.place(x=random_x, y=random_y, anchor="center")


def start_test():
    timer.start()
    start_button.place_forget()
    button.place(x=width//2, y=50, anchor="center")

button = tk.Button(window, text="Target", width=8, height=2, highlightbackground='#3E4149', fg="white", font=("Arial", 15),command=place_button_randomly)

start_button = tk.Button(window, text="Start", width=10, height=2, highlightbackground='red', bg='red', fg="white", font=("Arial", 20),command=start_test)
start_button.place(x=width//2, y=height//2+75, anchor="center")

def mouseover(event):
    log.write("Mouseover " + str(timer.checkpoint()) + "\n")

def key(event):
    window.event_generate('<Motion>', warp=True, x=width//2, y=height//2)

window.bind('<space>', key)

button.bind("<Enter>", mouseover)

window.geometry(f'{width}x{height}-5+40')
window.mainloop()