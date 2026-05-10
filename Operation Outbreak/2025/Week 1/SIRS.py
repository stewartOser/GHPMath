from simulation import Model, run_simulation

model = Model("SIRS Model")

SUSCEPTIBLE = model.add_state("Susceptible", (52, 152, 219), 999)
INFECTED    = model.add_state("Infected",    (231, 76, 60),    1,     effect_radius=7, show_cloud=True)
RECOVERED   = model.add_state("Recovered",   (142, 68, 173))

model.add_transition(
    SUSCEPTIBLE,
    INFECTED,
    probability=0.03,
    requires_proximity=True,
    contact_with=INFECTED,
    )

model.add_transition(
    INFECTED,
    RECOVERED,
    probability=0.005
    )

model.add_transition(
    RECOVERED,
    SUSCEPTIBLE,
    probability=0.005
)

if __name__ == "__main__":
    run_simulation(model)