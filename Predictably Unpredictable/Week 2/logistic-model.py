from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.pyplot as plt
import numpy as np

WIDTH = 1250
HEIGHT = 600

class AnimatePlot():
    def __init__(self, startN=0, endN=100):
        self.fig, self.ax = plt.subplots(figsize=(WIDTH / 100, HEIGHT / 100), dpi = 100)
        self.startN = startN
        self.endN = endN
        self.n_vals = np.array([i for i in range(self.startN, self.endN+1)])
        self.x_vals = [0] * len(self.n_vals)
        self.x_init = 0.1
        
        self.start = float(input("r starts at? "))
        self.end = float(input("r ends at? "))
        
    def generate_plot(self, frame):
        x = self.x_init
        [line_collection.remove() for line_collection in self.ax.collections]
        
        for i in range(1, self.startN):
            x = frame*x*(1 - x)
            
        for i in range(len(self.n_vals)):
            x = frame*x*(1 - x)
            self.x_vals[i]= x
                
        self.line.set_data(self.n_vals, self.x_vals)
        self.ax.set_title(f"R = {round(frame, 7)}")
        
        for x in self.x_vals:
            self.ax.hlines(x, self.startN, self.endN, color='red')
            print(x)
            
        return self.line,
            
    def render(self,x_init=0.1):
        self.x_init = x_init
        self.line, = self.ax.plot(self.n_vals, self.x_vals, 'bo-')
        self.ax.set_xlim(self.startN, self.endN)
        self.ax.set_ylim(0, 1)

        # set the range for the r-values in the np.linspace argument
        # for example for range 0-4 -> np.linspace(0, 4, 100)
        # or just to look at r=4 -> np.linspace(4,4,100)
        # as current, can provide range through cmd input
        self.ani = FuncAnimation(self.fig, self.generate_plot, frames=np.linspace(self.start, self.end, 500), interval=50, blit=False)
        plt.show(block=True)
        
plot = AnimatePlot(startN=300, endN=400)

# in the render command, first argument is x_init
# default is 0.1
plot.render(x_init=0.1)