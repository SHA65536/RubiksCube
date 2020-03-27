import matplotlib.pyplot as plt

x = []
y = []

with open("output.log",'r') as f:
        for count, line in enumerate(f):
            _, cycles = line.split("\t")
            x.append(count)
            y.append(cycles)

plt.scatter(x, y, s=0.5)
plt.show()