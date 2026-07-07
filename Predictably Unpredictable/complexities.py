import matplotlib.pyplot as plt

z = complex(0.7, 0.6)
c = complex(0, 1)
# print(z)

zLst = []
zLst.append(z)

for i in range(30):
    z = z**2
    print(z)
    zLst.append(z)
    
zReal = []
zImag = []

for num in zLst:
    zReal.append(num.real)
    zImag.append(num.imag)
    
plt.plot(zReal, zImag)
plt.show()