import math
import tkinter as tk

import pygame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

WIDTH = 800
HEIGHT = 800


class CobwebPlot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cobweb Diagram")
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="white")

        self.make_plot()

        self.canvas.pack()

        return

    def make_plot(self):
        fig = Figure(figsize=(WIDTH / 100, HEIGHT / 100), dpi=100)
        ax = fig.add_subplot(111)

        x = [i / 100 for i in range(1001)]
        y = [math.sin(i) for i in x]
        ax.plot(x, y)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def load_gui(self):
        self.root.mainloop()


if __name__ == "__main__":
    plot = CobwebPlot()
    plot.make_plot()
    plot.load_gui()
