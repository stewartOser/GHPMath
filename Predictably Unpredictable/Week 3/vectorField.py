import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def dx(x, y):
    return 1*x - 1*x*y

def dy(x, y):
    return -1*y + 1*x*y

class VectorField:
    def __init__(self, x, y, lowLimX, lowLimY, upLimX, upLimY):
        self.lowLimX = lowLimX
        self.lowLimY = lowLimY
        self.upLimX = upLimX
        self.upLimY = upLimY
        self.lineStartX = x
        self.lineStartY = y
        self.x = np.linspace(self.lowLimX, self.upLimX, 50)
        self.y = np.linspace(self.lowLimY, self.upLimY, 50)
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
            
            if x > self.upLimX or y > self.upLimY:
                break
            
            if x < self.lowLimX or y < self.lowLimY:
                break
        
        self.line.set_data(self.x_lst, self.y_lst)
        return self.line
        
    def render(self):
        self.ani = FuncAnimation(self.fig, self.plot_path, frames=10000, interval=5, blit=False, repeat=False)
        plt.show(block=True)

# for you, the parameters into VectorField are just numbers, not lists  
vec = VectorField(4, 2, 0, 0, 4.5, 4.5)
vec.draw_plot()
vec.render()