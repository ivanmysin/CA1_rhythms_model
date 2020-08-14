import numpy as np
import matplotlib.pyplot as plt 

phases = np.linspace(-np.pi, np.pi, 500)
y = np.cos(phases)

plt.plot(phases, y)
plt.show()

"""
rng = np.random.default_rng()
mean_x = 0.0001

x = rng.lognormal(np.log(mean_x), 0.5, 1000)



print( np.std(x) )

plt.hist(x, bins=30)
plt.show()

"""
