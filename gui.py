import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font

window = tk.Tk()
window.title("Python GUI")
width = 500
height = 390

button = tk.Button(text="Click me!", width=10, height=2, bg="blue", fg="blue", font=("Arial", 20))
label = tk.Label(text="Press the spacebar to start the experiment", font=("Arial", 20))

def mouseover(event):
    print("mouse over button")

def key(event):
    window.event_generate('<Motion>', warp=True, x=width//2, y=height//2)

window.bind('<space>', key)

button.bind("<Enter>", mouseover)
button.pack()

window.geometry(f'{width}x{height}-5+40')
window.mainloop()