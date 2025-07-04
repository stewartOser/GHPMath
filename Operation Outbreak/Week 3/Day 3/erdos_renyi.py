from simulation_network import run_simulation, Network
from SVIR_network import model
import random

n = 100
p = 0.12

nw = Network(model)
nw.add_nodes(n)

for _ in range(90):
    node = nw.random_node("Susceptible")
    nw.set_state(node, "Vaccinated")

patient_zero = nw.random_node("Susceptible")
nw.set_state(patient_zero, "Infected")

for i in range(1, n + 1):
    for j in range(i + 1, n + 1):
        if random.random() < p:
            nw.add_edges((i, j))

run_simulation(model, nw, num_frames=10, show_labels=False, display_stats=True)