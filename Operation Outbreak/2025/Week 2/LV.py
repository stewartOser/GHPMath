import matplotlib.pyplot as plt

t = 0           # initial time
R = 1000        # initial population of rabbits
W = 40          # initial population of wolves

dt = 0.01       # time step
t_final = 500    # final time

t_values = [t]  # list of times
R_values = [R]  # list of rabbit populations
W_values = [W]  # list of wolf populations

while t <= t_final:
    # Calculate small change in population
    dR = (0.08 * R * (1 - 0.0002 * R) - 0.001 * R * W) * dt
    dW = (-0.02 * W + 0.00002 * R * W) * dt

    t += dt     # update time
    R += dR     # update rabbit population
    W += dW     # update wolf population

    t_values.append(t)  # add time to end of list
    R_values.append(R)  # add rabbit population to end of list
    W_values.append(W)  # add wolf population to end of list

# plt.plot(t_values, R_values, label="Rabbits")
# plt.plot(t_values, W_values, label="Wolves")
# # plt.xlabel("Time")
# plt.ylabel("Population")

plt.plot(R_values, W_values)
plt.xlabel("Rabbits")
plt.ylabel("Wolves")
plt.title("Lotka-Volterra predator-prey model")

# plt.xlim((-5,20))
# plt.ylim((-10,30))

plt.legend()
plt.show()