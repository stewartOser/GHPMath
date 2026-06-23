import matplotlib.pyplot as plt
import numpy as np

starting_iter = 1000
ending_iter = 1500

start = 0
end = 4

class ZoomableBifurcation():
    def __init__(self):
        self.start = 0
        self.end = 4
        
        self.fig, self.ax = plt.subplots()
        
    def generate_plot(self):
        self.r_vals = np.linspace(self.start, self.end, ending_iter - starting_iter)
        self.x_vals = np.empty((ending_iter - starting_iter, len(self.r_vals)+1))

        x = 0.1
        index = 0
        for r in self.r_vals:
            x = 0.1
            x_list = []
            for i in range(0, starting_iter+1):
                x = r*x*(1-x)
            
            for i in range(starting_iter, ending_iter+1):
                x = r*x*(1-x)
                x_list.append(x)
                
            self.x_vals[index] = x_list
            index += 1

        self.ax.plot(self.r_vals, self.x_vals, 'ro', markersize=0.1)
        
    def main(self):
        self.generate_plot()
        self.fig.canvas.mpl_connect('button_release_event', self.redraw)
        self.fig.canvas.mpl_connect('button_release_event', self.redraw)

        plt.show()

    def redraw(self, event):
        xlim = self.ax.get_xlim()
        
        # self.ax.clear()
        
        self.start = float(xlim[0])
        self.end = float(xlim[1])
        
        self.r_vals = np.linspace(self.start, self.end, ending_iter - starting_iter)
        self.x_vals = np.empty((ending_iter - starting_iter, len(self.r_vals)+1))

        x = 0.1
        index = 0
        for r in self.r_vals:
            x = 0.1
            x_list = []
            for i in range(0, starting_iter+1):
                x = r*x*(1-x)
            
            for i in range(starting_iter, ending_iter+1):
                x = r*x*(1-x)
                x_list.append(x)
                
            self.x_vals[index] = x_list
            index += 1
        
        self.ax.plot(self.r_vals, self.x_vals, 'ro', markersize=0.1)
    
plot = ZoomableBifurcation()
plot.main()