import numpy as np
import matplotlib.pyplot as plt 




rng = np.random.default_rng()
mean_x = 0.0001

x = rng.vonmises(0, 0.5, 1000)


plt.hist(x, bins=30)
plt.show()



"""
phases = np.linspace(-np.pi, np.pi, 500)
y = np.cos(phases)

plt.plot(phases, y)
plt.show()
"""
