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
        
        self.lines = np.empty((self.endN-self.startN+1, 1))
        self.nVals = np.array([self.n_vals] * (len(self.n_vals)-1))
        
    def generate_plot(self, frame):
        x = self.x_init
        self.lines = np.empty((self.endN-self.startN, 1))

        
        print(self.x_vals)
        
        for i in range(1, self.startN):
            x = frame*x*(1 - x)
            
        for i in range(len(self.n_vals)):
            x = frame*x*(1 - x)
            self.x_vals[i]= x
            
        for x in self.x_vals:
            x_list = [x] * (len(self.n_vals)-1)
            l_vals = np.array(x_list)
            self.lines = np.append(self.lines, l_vals.reshape(-1, 1), axis=1)
            
        self.lines = self.lines[:,1:]
        print(self.lines)
                
        self.line.set_data(self.n_vals, self.x_vals)
        self.lineVals.set_data(self.nVals.flatten(), self.lines.flatten())
        self.ax.set_title(f"R = {round(frame, 7)}")
        return self.line, self.lineVals,
            
    def render(self,x_init=0.1):
        self.x_init = x_init
        self.line, = self.ax.plot(self.n_vals, self.x_vals, 'bo-')
        self.lineVals, = self.ax.plot([], [], 'r-')
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
