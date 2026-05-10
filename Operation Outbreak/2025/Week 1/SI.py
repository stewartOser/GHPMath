from simulation import Model, run_simulation

model = Model("SI Model")

SUSCEPTIBLE = model.add_state("Susceptible", (52, 152, 219), 999)
INFECTED    = model.add_state("Infected",    (231, 76, 60),    1,     effect_radius=7, show_cloud=True)

model.add_transition(
    SUSCEPTIBLE,
    INFECTED,
    probability=0.03,
    requires_proximity=True,
    contact_with=INFECTED,
    )

if __name__ == "__main__":
    run_simulation(model)