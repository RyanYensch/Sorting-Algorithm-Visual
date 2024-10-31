from tkinter import *
import random


WINDOW_HEIGHT = 500
WINDOW_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 600
NUM_BARS = 100


class Sorting_Visualiser:
    def __init__(self):
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.num_bars = NUM_BARS
        self.bar_heights = [random.randint(10, self.screen_height) for _ in range(self.num_bars)]

        self.window = Tk()
        self.window.title("Sorting Program")
        self.window.geometry(f"{self.window_width}x{self.window_height}")

        self.canvas = Canvas(self.window, width=self.screen_width, height=self.screen_height, bg="black")
        self.canvas.pack()

    def draw_bars(self):
        self.canvas.delete("all")
        bar_width = self.screen_width / self.num_bars

        for i, height in enumerate(self.bar_heights):
            x0 = i * bar_width
            x1 = (i + 1) * bar_width
            y0 = self.screen_height
            y1 = self.screen_height - height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="green")

    def run(self):
        self.draw_bars()
        self.window.mainloop()


visualiser = Sorting_Visualiser()
visualiser.run()