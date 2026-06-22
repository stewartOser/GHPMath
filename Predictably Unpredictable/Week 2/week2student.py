import matplotlib.pyplot as plt

WIDTH = 1250
HEIGHT = 600

start = 0
end = 100

n_vals = [i for i in range(start, end+1)]

x_vals = [0] * len(n_vals)

fig, ax = plt.subplots(figsize=(WIDTH / 100, HEIGHT / 100), dpi = 100)

def generate_plot(r=2, x_init=0.1):
    x = x_init
    for i in range(len(n_vals)):
            x = r*x*(1 - x)
            x_vals[i]= x
            
    ax.plot(n_vals, x_vals, 'bo-')
    plt.show()
    
generate_plot(r=4, x_init=0.2)