from simulation import Model, run_simulation

model = Model("SEIR Model")

SUSCEPTIBLE = model.add_state("Susceptible", (52, 152, 219), 999)
EXPOSED     = model.add_state("Exposed",     (26, 188, 156),      effect_radius=10, show_cloud=True)
INFECTED    = model.add_state("Infected",    (231, 76, 60),    1, effect_radius=10, show_cloud=True)
RECOVERED   = model.add_state("Recovered",   (142, 68, 173))


model.add_transition(
    SUSCEPTIBLE,
    EXPOSED,
    probability=0.03,
    requires_proximity=True,
    contact_with=INFECTED,
    )

model.add_transition(
    SUSCEPTIBLE,
    EXPOSED,
    probability=0.03,
    requires_proximity=True,
    contact_with=EXPOSED,
    )

model.add_transition(
    EXPOSED,
    INFECTED,
    probability=0.01
    )

model.add_transition(
    INFECTED,
    RECOVERED,
    probability=0.002
    )

if __name__ == "__main__":
    run_simulation(model)