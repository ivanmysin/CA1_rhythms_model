import numpy as np
import matplotlib.pyplot as plt 

rng = np.random.default_rng()
mean_x = 0.0001

x = rng.lognormal(np.log(mean_x), 0.5, 1000)



print( np.std(x) )

plt.hist(x, bins=30)
plt.show()

