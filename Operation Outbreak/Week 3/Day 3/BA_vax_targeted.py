from simulation_network import run_simulation, Network
from SVIR_network import model
import random

n = 500
m = 1
assert m < n

nw = Network(model)
nw.add_nodes(n)

# Set 20 highest-degree nodes to "Vaccinated"
degrees = [(node, nw.degree(node)) for node in nw.graph.nodes]
degrees.sort(key=lambda x: x[1], reverse=True)
top_20_nodes = [node for node, deg in degrees[:20]]
for node in top_20_nodes:
    if nw.get_state(node) == "Susceptible":
        nw.set_state(node, "Vaccinated")

# Set random node to "Infected"
nw.set_state(nw.random_node("Susceptible"),"Infected")

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

run_simulation(model, nw, num_frames=30, show_labels=False, display_stats=True)