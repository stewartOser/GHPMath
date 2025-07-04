import matplotlib.pyplot as plt

t = 0           # initial time
P = 10          # initial population

k = 0.6         # rate constant
N = 20          # carrying capacity
h = 3           # harvesting rate

dt = 0.01       # time step
t_final = 15    # final time

t_values = [t]  # list of times
P_values = [P]  # list of populations
while t <= t_final:
    # Calculate small change in population
    dP = (k * P * (1 - P/N) - h) * dt

    t += dt     # update time
    P += dP     # update population

    t_values.append(t)  # add time to end of list
    P_values.append(P)  # add population to end of list

plt.plot(t_values, P_values, label="Population")
plt.xlabel("Time")
plt.ylabel("Population")
plt.title("Unrestricted population growth")
# plt.xlim((-5,20))
plt.ylim((-10,30))

plt.legend()
plt.show()