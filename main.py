from tkinter import *
import random


WINDOW_HEIGHT = 500
WINDOW_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 600
NUM_BARS = 100
DELAY = 10


class Sorting_Visualiser:
    def __init__(self):
        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.num_bars = NUM_BARS

        self.window = Tk()
        self.window.title("Sorting Program")
        self.window.geometry(f"{self.window_width}x{self.window_height}")

        self.canvas = Canvas(self.window, width=self.screen_width, height=self.screen_height, bg="black")
        self.canvas.pack()
    
    def randomise_bars(self):
        self.bar_heights = [i * SCREEN_HEIGHT / self.num_bars for i in range(1, self.num_bars + 1)]
        random.shuffle(self.bar_heights)

    def draw_bars(self, array, changed1 = -1, changed2 = -1):
        self.canvas.delete("all")
        bar_width = self.screen_width / self.num_bars

        for i, height in enumerate(array):
            x0 = i * bar_width
            x1 = (i + 1) * bar_width
            y0 = self.screen_height
            y1 = self.screen_height - height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=("white" if (i == changed1 or i == changed2) else "green"))

    def next_step(self, array, changed1, changed2):
        self.window.update_idletasks()
        self.window.after(DELAY)
        self.draw_bars(array, changed1, changed2)
        

    def bubble_sort(self):
        self.window.update_idletasks()
        for i in range(len(self.bar_heights)):
            for j in range(len(self.bar_heights) - i - 1):
                if self.bar_heights[j] > self.bar_heights[j + 1]:
                    temp = self.bar_heights[j]
                    self.bar_heights[j] = self.bar_heights[j + 1]
                    self.bar_heights[j + 1] = temp
                    self.next_step(self.bar_heights, j, j+1)


    def run(self):
        self.randomise_bars()
        self.draw_bars(self.bar_heights)
        self.window.after(1000, self.bubble_sort())
        self.window.mainloop()


visualiser = Sorting_Visualiser()
visualiser.run()