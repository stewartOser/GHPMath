from simulation_network import run_simulation, Network
from SIR_network import model
import random

n = 50
p = 0.12

nw = Network(model)
nw.add_nodes(n)

for i in range(1, n + 1):
    for j in range(i + 1, n + 1):
        if random.random() < p:
            nw.add_edges((i, j))

run_simulation(model, nw, num_frames=10, show_labels=False, display_stats=True)