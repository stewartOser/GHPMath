from simulation_network import run_simulation, Network
from SIR_network import model
import random

n = 50
k = 10
p = 0.05

nw = Network(model)
nw.add_nodes(n)

for i in range(n):
    for j in range(1, k // 2 + 1):
        neighbor = (i + j) % n
        if neighbor != i:
            nw.add_edges((i + 1, neighbor + 1))

for i in range(n):
    for j in range(1, k // 2 + 1):
        neighbor = (i + j) % n
        if neighbor != i:
            if random.random() < p:
                current_node = i + 1
                all_nodes = set(range(1, n + 1))
                current_neighbors = set(nw.neighbors(current_node))
                possible = all_nodes - {current_node} - current_neighbors
                if possible:
                    new_neighbor = random.choice(list(possible))
                    if 1 <= neighbor + 1 <= n and nw.graph.has_edge(current_node, neighbor + 1):
                        nw.remove_edge(current_node, neighbor + 1)
                        if 1 <= new_neighbor <= n and 1 <= current_node <= n:
                            nw.add_edges((current_node, new_neighbor))

run_simulation(model, nw, num_frames=10, show_labels=False, display_stats=True)