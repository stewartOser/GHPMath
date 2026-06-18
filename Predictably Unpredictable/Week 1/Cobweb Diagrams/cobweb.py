import math
# import tkinter as tk
import time

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

WIDTH = 800
HEIGHT = 600

class CobwebPlot:
    def __init__(self, function):
        #self.root = tk.Tk()
        #self.root.title("Cobweb Diagram")

        self.function = function

        #self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT)
        self.x_vals = []
        self.y_vals = []

    def generate_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(WIDTH / 100, HEIGHT / 100), dpi=100)

        self.x = [i/100 for i in range(0, 100)]
        self.y = [self.function(i) for i in self.x]

        self.ax.plot(self.x, self.y)
        self.ax.plot(self.x, self.x, color='red')

        line = self.ax.plot(self.x_vals, self.y_vals, color='black')

        #canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        #canvas.draw()
        #canvas.get_tk_widget().pack()

    def load_gui(self):
        self.generate_plot()
        #self.root.mainloop()

    def get_point(self, x):
        self.val = self.function(x)

        return self.val
    
    def start_web(self, frame):
        if frame == 0:
            x = self.x_init
            y = self.function(self.x_init)
            self.x_vals = [x,x,y]
            self.y_vals = [0,y,y]
            self.last_y = self.y_vals[2]
        else:
            next_x = self.last_y
            next_y = self.function(next_x)
            self.x_vals += [next_x,next_y]
            self.y_vals += [next_y,next_y]
            self.last_y = next_y

        self.web_line.set_data(self.x_vals, self.y_vals)
        return self.web_line,

    def render(self, x_init=0.1):
        self.x_init = x_init
        self.x_vals = [x_init]
        self.y_vals = [self.function(x_init)]
        self.last_y = self.y_vals[0]
        self.web_line, = self.ax.plot(self.x_vals, self.y_vals, color='black')

        self.ani = FuncAnimation(self.fig, self.start_web, frames=21, interval=200, blit=False)
        plt.show(block=True)
    

if __name__ == "__main__":
    def func(x):
        return 4*x*(1-x)
    
    plot = CobwebPlot(func)
    plot.load_gui()
    plot.render()