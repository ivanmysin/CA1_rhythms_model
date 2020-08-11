import numpy as np
import matplotlib.pyplot as plt
from scipy.special import i0 as bessel

def my_vonmises(mu, kappa, size):
    
    I0 = bessel(kappa)
    
    angles = np.empty(shape=size, dtype=np.float)
    
    idx = 0
    phase = 0
    while idx < size:
        
        phase += 0.001
        
        pdf = np.exp(kappa * np.cos(phase - mu) ) / (2 * np.pi * I0)
        # print(pdf)
        if pdf*0.001 > np.random.rand():
            angles[idx] = phase
            idx += 1
            

    return angles



Rsetted = 0.2

if Rsetted < 0.53:
    kappa = 2 * Rsetted + Rsetted**3 + 5/6 * Rsetted**5

elif Rsetted >= 0.53 and Rsetted < 0.85:
    kappa = -0.4 + 1.39 * Rsetted + 0.43 / (1 - Rsetted)

elif Rsetted >= 0.85:
    kappa = 1 / (3*Rsetted - 4*Rsetted**2 + Rsetted**3)

print(kappa)

I0 = bessel(kappa)
print(I0)


"""
mu = -2.5
angles = my_vonmises (mu, kappa, 1000) # np.random.vonmises

spike_train = 5 * angles * 0.5 / np.pi
# print(angles[-1])

mean_vect_x = np.mean( np.cos(angles) )
mean_vect_y = np.mean( np.sin(angles) )

mu_calc = np.arctan2(mean_vect_y, mean_vect_x)
Rcalc = np.sqrt(mean_vect_x**2 + mean_vect_y**2)


print(mu_calc)

y = np.ones_like(spike_train)

plt.scatter(spike_train, y)
plt.show()
"""

    




