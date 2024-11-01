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
        self.draw_bars(self.bar_heights)

    def draw_bars(self, array, changed1 = -1, changed2 = -1, sorted=False, entry = -1):
        self.canvas.delete("all")
        bar_width = self.screen_width / self.num_bars

        for i, height in enumerate(array):
            x0 = i * bar_width
            x1 = (i + 1) * bar_width
            y0 = self.screen_height
            y1 = self.screen_height - height
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=("white" if (i == changed1 or i == changed2 or (sorted == True and i <= entry)) else "green"))

    def next_step(self, array, changed1 = -1, changed2 = -1, sorted = False):
        self.window.update_idletasks()
        self.window.update()
        self.window.after(DELAY)
        self.draw_bars(array, changed1, changed2, sorted)
    
    def draw_sorted(self, array, i = 0):
        self.window.update_idletasks()
        self.window.update()
        if (i < len(array)):
            self.draw_bars(array, sorted=True, entry=i)
            self.window.after(DELAY * 2, self.draw_sorted(array, i + 1))
        else:
            self.draw_bars(array)

    def bubble_sort(self, array):
        self.window.update_idletasks()
        for i in range(len(array)):
            for j in range(len(array) - i - 1):
                if array[j] > array[j + 1]:
                    (array[j], array[j + 1]) = (array[j + 1], array[j])
                    self.next_step(array, j, j+1)
        
        self.draw_sorted(array)

    def selection_sort(self, array):
        for i in range(len(array)):
            min = i

            for j in range(i + 1, len(array)):
                if (array[j] < array[min]):
                    self.next_step(array, j, min)
                    min = j
            (array[i], array[min]) = (array[min], array[i])
            self.next_step(array, i, min)

        self.draw_sorted(array)

    def insertion_sort(self, array):
        n = len(array)

        for i in range(1, n):
            key = array[i]
            j = i - 1

            while (j >= 0 and key < array[j]):
                array[j + 1] = array[j]
                j -= 1
                self.next_step(array, j, j + 1)

            array[j + 1] = key
            self.next_step(array, i, j + 1)

        self.draw_sorted(array)    

    def add_buttons(self):
        self.button_frame = Frame(self.window)
        self.button_frame.pack()
        self.random_button = Button(self.button_frame, text="Randomise", font="arial", command=self.randomise_bars)
        self.random_button.grid(row=0, column=0)
        self.bubble_button = Button(self.button_frame, text="Bubble Sort", font="arial", command=lambda: self.bubble_sort(self.bar_heights))
        self.bubble_button.grid(row=0, column=1)
        self.selection_button = Button(self.button_frame, text="Selection Sort", font="arial", command=lambda: self.selection_sort(self.bar_heights))
        self.selection_button.grid(row=0, column=2)
        self.insertion_button = Button(self.button_frame, text="Insertion Sort", font="arial", command=lambda: self.insertion_sort(self.bar_heights))
        self.insertion_button.grid(row=0, column=3)

    def run(self):
        self.randomise_bars()
        self.draw_bars(self.bar_heights)
        self.add_buttons()
        self.window.mainloop()


visualiser = Sorting_Visualiser()
visualiser.run()