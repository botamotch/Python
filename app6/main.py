import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
axs = fig.add_subplot(111)

xp = np.arange(-1, 1, 0.1)

line = []
for i in range(8):
    line.append(axs.plot([], [], color='blue')[0])

for i, l in enumerate(line):
    l.set_data([-1, 0, 1], [(-1) ** i, (-1) ** (i//2), (-1) ** (i//4)])
    # l.set_data(xp, f(xp, i))

axs.set_xlim((-1, 1))
axs.set_ylim((-1.5, 1.5))
plt.show()

