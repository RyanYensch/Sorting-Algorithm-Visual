from tkinter import *
import numpy as np
import sounddevice as sd
import random


WINDOW_HEIGHT = 500
WINDOW_WIDTH = 600
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 600
NUM_BARS = 100
DELAY = 5

def normalize_frequency(input_value, min_freq=100, max_freq=500):
    normalized_value = (input_value - 1) / (NUM_BARS - 1)
    return min_freq + normalized_value * (max_freq - min_freq)

def play_tone(freq, dur):
    volume = 0.1
    sample_rate = 44100
    freq = normalize_frequency(freq)
    t = np.linspace(0, dur, int(sample_rate * dur), endpoint = False)
    fade_out = np.linspace(1, 0, int(sample_rate * dur))
    tone = volume * 0.5 * np.sin(2 * np.pi * freq * t) * fade_out
    sd.play(tone, samplerate=sample_rate, blocking=True, blocksize=2048)


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
        play_tone(array[changed1], 0.1)
        self.draw_bars(array, changed1, changed2, sorted)
    
    def draw_sorted(self, array, i = 0):
        self.window.update_idletasks()
        self.window.update()
        if (i < len(array)):
            self.draw_bars(array, sorted=True, entry=i)
            play_tone(array[i], 0.1)
            self.window.after(DELAY * 0.5, self.draw_sorted(array, i + 1))
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

    def merge_sort(self, array, left_index=0, right_index=None):
        if right_index is None:
            right_index = len(array) - 1

        if left_index < right_index:
            mid_index = (left_index + right_index) // 2 

            self.merge_sort(array, left_index, mid_index)
            self.merge_sort(array, mid_index + 1, right_index)

            self.merge(array, left_index, mid_index, right_index)

    def merge(self, array, left_index, mid_index, right_index):
        L = array[left_index:mid_index + 1]
        M = array[mid_index + 1:right_index + 1]

        i = j = 0
        k = left_index

        while i < len(L) and j < len(M):
            self.next_step(array, left_index + i, mid_index + 1 + j)
            
            if L[i] < M[j]:
                array[k] = L[i]
                i += 1
            else:
                array[k] = M[j]
                j += 1
            k += 1

        while i < len(L):
            array[k] = L[i]
            i += 1
            k += 1

        while j < len(M):
            array[k] = M[j]
            j += 1
            k += 1

        self.next_step(array, left_index, right_index)


    def quick_sort(self, array, low=0, high=None):
        if high is None:
            high = len(array) - 1
        if low < high:
            pivot_index = self.partition(array, low, high)
            
            self.quick_sort(array, low, pivot_index - 1)
            self.quick_sort(array, pivot_index + 1, high)

    def partition(self, array, low, high):
        pivot = array[high]
        i = low - 1

        for j in range(low, high):
            self.next_step(array, j, high)

            if array[j] < pivot:
                i += 1
                array[i], array[j] = array[j], array[i]

        array[i + 1], array[high] = array[high], array[i + 1]
        return i + 1

    def add_buttons(self):
        self.button_frame = Frame(self.window)
        self.button_frame.pack()
        self.random_button = Button(self.button_frame, text="Randomise", font="arial", command=self.randomise_bars)
        self.random_button.grid(row=0, column=0, columnspan=5)
        self.bubble_button = Button(self.button_frame, text="Bubble Sort", font="arial", command=lambda: self.bubble_sort(self.bar_heights))
        self.bubble_button.grid(row=1, column=0)
        self.selection_button = Button(self.button_frame, text="Selection Sort", font="arial", command=lambda: self.selection_sort(self.bar_heights))
        self.selection_button.grid(row=1, column=1)
        self.insertion_button = Button(self.button_frame, text="Insertion Sort", font="arial", command=lambda: self.insertion_sort(self.bar_heights))
        self.insertion_button.grid(row=1, column=2)
        self.merge_button = Button(self.button_frame, text="Merge Sort", font="arial", command=lambda: self.merge_sort(self.bar_heights))
        self.merge_button.grid(row=1, column=3)
        self.quick_button = Button(self.button_frame, text="Quick Sort", font="arial", command=lambda: self.quick_sort(self.bar_heights))
        self.quick_button.grid(row=1, column=4)


    def run(self):
        self.randomise_bars()
        self.draw_bars(self.bar_heights)
        self.add_buttons()
        self.window.mainloop()


visualiser = Sorting_Visualiser()
visualiser.run()