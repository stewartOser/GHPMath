from simulation_network import run_simulation, Network
from SIR_network import model
# Note lowercase on "model"; we're importing the actual model instance, not the class

nw = Network(model)
nw.add_nodes(5, "Susceptible")   # Add 5 nodes with initial state "Susceptible"
nw.set_state(0, "Infected")      # Initial state for node 0

for i in range(5):
    for j in range(i + 1, 5):
        nw.add_edges((i, j))  # Fully connect the nodes

# Show how to print information about the underlying graph
g = nw.get_nx_graph()
print(g.nodes)

print(g.degree())

run_simulation(model, nw, num_frames=10)