from tkinter import *
import random


WINDOW_HEIGHT = 500
WINDOW_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 600
NUM_BARS = 100


window = Tk()
window.title("Sorting Program")
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

canvas = Canvas(window, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="black")
canvas.pack()

bar_heights = [random.randint(10, 400) for _ in range(NUM_BARS)]

def draw_bars():
    canvas.delete("all")
    bar_width = (SCREEN_WIDTH) / NUM_BARS

    for i, height in enumerate(bar_heights):
        x0 = i * (bar_width)
        x1 = (i + 1) * bar_width
        y0 = SCREEN_HEIGHT
        y1 = SCREEN_HEIGHT - height
        canvas.create_rectangle(x0, y0, x1, y1, fill="green")

draw_bars()

window.mainloop()