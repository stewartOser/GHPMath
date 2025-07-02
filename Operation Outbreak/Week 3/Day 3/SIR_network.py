from simulation_network import Model

# Define the SIR model
model = Model("SIR Network Model")

SUSCEPTIBLE = model.add_state("Susceptible", (52, 152, 219), default=True)
INFECTED    = model.add_state("Infected",    (231, 76, 60))
RECOVERED   = model.add_state("Recovered",   (142, 68, 173))

model.add_transition(
    SUSCEPTIBLE,
    INFECTED,
    probability=1,
    requires_proximity=True,
    contact_with=INFECTED,
)

model.add_transition(
    INFECTED,
    RECOVERED,
    probability=1
)