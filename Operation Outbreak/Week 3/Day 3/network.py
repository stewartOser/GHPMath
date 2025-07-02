from simulation_network import run_simulation, Network
from SIR_network import model

nw = Network(model)

nw.add_nodes(6)
nw.set_state(1, "Infected")

nw.add_edges(
    (1,2),
    (1,3),
    (3,4),
    (4,5),
    (3,6),
    (3,5),
    (4,5),
    (5,6)
)

run_simulation(model, nw, num_frames=10, layout="circular")