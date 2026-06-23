from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.pyplot as plt
import numpy as np

WIDTH = 1250
HEIGHT = 600

class AnimatePlot():
    def __init__(self, startN=0, endN=100):
        self.fig, (self.ax, self.bif_ax) = plt.subplots(
            1,
            2,
            figsize=(WIDTH / 100, HEIGHT / 100),
            dpi=100,
            gridspec_kw={"width_ratios": [1, 1]},
        )
        self.startN = startN
        self.endN = endN
        self.n_vals = np.array([i for i in range(self.startN, self.endN+1)])
        self.x_vals = [0] * len(self.n_vals)
        self.x_init = 0.1
        
        self.start = float(input("r starts at? "))
        self.end = float(input("r ends at? "))
        # Accumulated points for the bifurcation diagram.
        # These are never cleared, so the right-hand plot gradually fills in.
        self.bif_r_vals = []
        self.bif_x_vals = []
        
    def generate_plot(self, frame):
        x = self.x_init
        [line_collection.remove() for line_collection in self.ax.collections]
        
        # Skip the transient behavior so that we only see the long-term dynamics.
        for i in range(1, self.startN):
            x = frame*x*(1 - x)
            
        # Compute the iterates that will be shown on the left-hand plot.
        for i in range(len(self.n_vals)):
            x = frame*x*(1 - x)
            self.x_vals[i]= x
                
        self.line.set_data(self.n_vals, self.x_vals)
        self.ax.set_title(f"r = {round(frame, 7)}", loc="left")
        
        # Draw horizontal guides on the iterate plot and simultaneously
        # add the corresponding (r, x) points to the bifurcation diagram.
        for x in self.x_vals:
            self.ax.hlines(x, self.startN, self.endN, color="red", alpha=0.35)
            self.bif_r_vals.append(frame)
            self.bif_x_vals.append(x)

        self.bif_points.set_data(self.bif_r_vals, self.bif_x_vals)

        return self.line, self.bif_points
            
    def render(self, x_init=0.1):
        self.x_init = x_init
        # Left plot: Iterates x_n versus n.
        self.line, = self.ax.plot(self.n_vals, self.x_vals, "bo-", markersize=3)
        # Right plot: Accumulated bifurcation points.
        self.bif_points, = self.bif_ax.plot([], [], "r.", markersize=1)
        self.ax.set_xlim(self.startN, self.endN)
        self.ax.set_ylim(0, 1)
        self.ax.set_xlabel("n")
        self.ax.set_ylabel("x")
        self.ax.set_title("Iterates")

        self.bif_ax.set_xlim(self.start, self.end)
        self.bif_ax.set_ylim(0, 1)
        self.bif_ax.set_xlabel("r")
        self.bif_ax.set_ylabel("x")
        self.bif_ax.set_title("Bifurcation diagram")

        self.fig.tight_layout()

        # Sweep through r-values from the requested start to end values.
        # Each frame updates the iterate plot and contributes points to
        # the bifurcation diagram.
        self.ani = FuncAnimation(
            self.fig,
            self.generate_plot,
            frames=np.linspace(self.start, self.end, 500),
            interval=50,
            blit=False,
            repeat=False,
        )
        plt.show(block=True)
        
def reanimate():
    plot = AnimatePlot(startN=900, endN=1000)
    # In the render command, the first argument is x_init.
    # The default is 0.1.
    plot.render(x_init=0.1)

plot = reanimate()

plot.ax.callbacks.connect('xlim_changed', reanimate)
plot.ax.callbacks.connect('ylim_changed', reanimate)