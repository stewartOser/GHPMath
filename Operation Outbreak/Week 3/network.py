from simulation_network import run_simulation, Network, OutbreakGraph
from SIR_network import model
import networkx as nx
# Note lowercase on "model"; we're importing the actual model instance, not the class

nw = Network(model)
nw.add_nodes(6, "Susceptible")   # Add 5 nodes with initial state "Susceptible"
nw.set_state(1, "Infected")      # Initial state for node 0

nw.add_edges(
    (1,2),
    (1,3),
    (3,4),
    (3,5),
    (4,5),
    (3,6),
    (4,5),
    (5,6)
)

# Show how to print information about the underlying graph
g = OutbreakGraph(nw.get_nx_graph())
print(g.degree())
print(g.average_degree_connectivity())
print(g.average_neighbor_degree())
print(g.average_degree())
print(g.node_degree(1))
# print(nx.average_degree_connectivity(g))
# print(g.nodes)

# print(g.degree())

run_simulation(model, nw, num_frames=10)