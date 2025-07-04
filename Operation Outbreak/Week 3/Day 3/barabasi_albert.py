from simulation_network import run_simulation, Network
from SVIR_network import model
import random

n = 500
m = 1
assert m < n

nw = Network(model)
nw.add_nodes(n)

for _ in range(90):
    node = nw.random_node("Susceptible")
    nw.set_state(node, "Vaccinated")

patient_zero = nw.random_node("Susceptible")
nw.set_state(patient_zero, "Infected")

for i in range(1, m + 2):
    for j in range(i + 1, m + 2):
        nw.add_edges((i, j))

for new_node in range(m + 2, n + 1):
    existing_nodes = list(nw.graph.nodes)
    degrees = [nw.degree(node) for node in existing_nodes]
    total_degree = sum(degrees)
    targets = set()

    while len(targets) < m:
        chosen = random.choices(existing_nodes, weights=degrees, k=1)[0]
        targets.add(chosen)

    for target in targets:
        nw.add_edges((new_node, target))

run_simulation(model, nw, num_frames=10, show_labels=False, display_stats=True)