import matplotlib.pyplot as plt

t = 0           # initial time
S = 900         # initial susceptible
I = 10          # initial infected
R = 0           # initial recovered

beta = 0.10      # infection rate
gamma = 0.04    # recovery rate
N = S+I+R       # total population

dt = 0.01       # time step
t_final = 200    # final time

t_values = [t]  # list of times
S_values = [S]  # list of susceptible
I_values = [I]  # list of infected
R_values = [R]  # list of recovered

while t <= t_final:
    # Calculate small change in population
    dS = (-beta * S * I / N) * dt
    dI = (beta * S * I / N - gamma * I) * dt
    dR = (gamma * I) * dt

    t += dt     # update time
    S += dS     # update susceptible
    I += dI     # update infected
    R += dR     # update recovered

    t_values.append(t)  # add time to end of list
    S_values.append(S)  # add susceptible to end of list
    I_values.append(I)  # add susceptible to end of list
    R_values.append(R)  # add susceptible to end of list

plt.plot(t_values, S_values, label="Susceptible")
plt.plot(t_values, I_values, label="Infected")
plt.plot(t_values, R_values, label="Recovered")
plt.xlabel("Time")
plt.ylabel("Population")
plt.title("SIR Model (Dynamical System)")
# plt.xlim((-5,20))
# plt.ylim((-10,30))

plt.legend()
plt.show()