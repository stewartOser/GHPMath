from simulation import Model, run_simulation

model = Model("SIRC Model")

SUSCEPTIBLE = model.add_state("Susceptible", (52, 152, 219), 999)
INFECTED    = model.add_state("Infected",    (231, 76, 60),    1, effect_radius=10, show_cloud=True)
RECOVERED   = model.add_state("Recovered",   (142, 68, 173))
CARRIER     = model.add_state("Carrier",     (46, 204, 113),      effect_radius=10, show_cloud=True)


model.add_transition(
    SUSCEPTIBLE,
    INFECTED,
    probability=0.03,
    requires_proximity=True,
    contact_with=INFECTED,
    )

model.add_transition(
    SUSCEPTIBLE,
    INFECTED,
    probability=0.03,
    requires_proximity=True,
    contact_with=CARRIER,
    )

model.add_transition(
    INFECTED,
    RECOVERED,
    probability=0.001
    )

model.add_transition(
    INFECTED,
    CARRIER,
    probability=0.001
    )

if __name__ == "__main__":
    run_simulation(model)