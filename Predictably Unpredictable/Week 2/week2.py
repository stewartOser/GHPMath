from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.pyplot as plt
import numpy as np

WIDTH = 800
HEIGHT = 600

class AnimatePlot():
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(WIDTH / 100, HEIGHT / 100), dpi = 100)
        self.steps = 30
        self.n_vals = [i for i in range(1, self.steps + 1)]
        self.x_vals = [0] * len(self.n_vals)
        self.x_init = 0.1
        
        self.start = int(input("r starts at? "))
        self.end = int(input("r ends at? "))
        
    def generate_plot(self, frame):
        print(frame)
        x = self.x_init
        for i in range(self.steps):
            x = frame*x*(1 - x)
            self.x_vals[i]= x
                
        self.line.set_data(self.n_vals, self.x_vals)
        return self.line,
            
    def render(self,x_init=0.1):
        self.x_init = x_init
        self.line, = self.ax.plot(self.n_vals, self.x_vals, 'bo-')
        self.ax.set_xlim(1, self.steps)
        self.ax.set_ylim(0, 1)

        # set the range for the r-values in the np.linspace argument
        # for example for range 0-4 -> np.linspace(0, 4, 100)
        # or just to look at r=4 -> np.linspace(4,4,100)
        # as current, can provide range through cmd input
        self.ani = FuncAnimation(self.fig, self.generate_plot, frames=np.linspace(self.start, self.end, 50), interval=500, blit=False)
        plt.show(block=True)
        
plot = AnimatePlot()

# in the render command, first argument is x_init
# default is 0.1
plot.render(x_init=0.1)
