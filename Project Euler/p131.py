# find all the primes
max = 1000000
lst = [True] * (max+1)
lst[0] = False
lst[1] = False
p = 2

while p * p <= max:
    if lst[p]:
        for i in range(p * p, max + 1, p):
            lst[i] = False
    p += 1

index = 0
primes = []
for i in lst:
    if i == True:
        primes.append(index)
        
    index += 1

cbdiff = []
for i in range(1, max):
    cbdiff.append(i**3 - (i - 1)**3)

primes = set(primes)
numPrimes = 0
for i in cbdiff:
    if i in primes:
        numPrimes += 1

print(numPrimes)