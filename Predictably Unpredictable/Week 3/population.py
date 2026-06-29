P = 100
t = 0

k = 0.2
t_final = 50

C = 1000

dt = 0.01

while t <= t_final:
    print(f"t = {t}\t P = {P}")
    
    # Calculate change in population
    dP = k * P * (1 - P/C) * dt
    
    # Update time and population
    t += dt
    P += dP