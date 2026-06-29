import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def dx(x, y):
    return x + y

def dy(x, y):
    return x*y

class VectorField:
    def __init__(self, x, y):
        self.lineStartX = x
        self.lineStartY = y
        self.x = np.linspace(-10, 10, 50)
        self.y = np.linspace(-10, 10, 50)
        self.X, self.Y = np.meshgrid(self.x, self.y)
        
        self.U = dx(self.X, self.Y)
        self.V = dy(self.X, self.Y)
    
        self.M = np.hypot(self.U, self.V)
        
        self.U = self.U / self.M
        self.V = self.V / self.M
        
        self.x_lst = []
        self.y_lst = []
        
    def draw_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 8), dpi=100)
        self.q = self.ax.quiver(self.X, self.Y, self.U, self.V, self.M, cmap="inferno")
        self.line, = self.ax.plot(self.x_lst, self.y_lst, color="black")
        
    def plot_path(self, frame):        
        dt = 0.01
        x = self.lineStartX
        y = self.lineStartY
        
        self.x_lst = []
        self.y_lst = []
        
        for _ in range(0, frame):       
            self.x_lst.append(x)
            self.y_lst.append(y)
            x += dx(x, y) * dt
            y += dy(x, y) * dt
            
            if x > 10 or y > 10:
                break
            
            if x < -10 or y < -10:
                break
        
        self.line.set_data(self.x_lst, self.y_lst)
        return self.line
        
    def render(self):
        self.ani = FuncAnimation(self.fig, self.plot_path, frames=1000, interval=5, blit=False)
        plt.show(block=True)

vec = VectorField(-2, 5)
vec.draw_plot()
vec.render()