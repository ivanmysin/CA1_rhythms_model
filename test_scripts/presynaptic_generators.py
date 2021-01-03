import numpy as np
import matplotlib.pyplot as plt
from scipy.special import i0 as bessel

# def get_grid_centers(grid_w, grid_phase, duration):
#     n_max = int(grid_w * duration + grid_phase / (2 * np.pi)) + 1
#
#     n = np.arange(0, n_max)
#     tgrid = (n - grid_phase / (2 * np.pi)) / grid_w
#
#     tgrid = tgrid[tgrid >= 0]
#     tgrid = tgrid[tgrid <= duration]
#
#     return tgrid
#
# grid_phases = np.linspace(-np.pi, np.pi, 100)
# gmax_arr = []
# for gphase in grid_phases:
#     grid_centers = 1000 * get_grid_centers(0.5, gphase, 3)
#     number_connections = 0
#     pyr_coord = 1500
#     gmax_tmp = 0
#     gmax = 1
#     var_conns_on_pyr = 100
#
#
#     for cent in grid_centers:
#         dist = pyr_coord - cent
#
#         dist_normalizer = np.exp(-0.5 * dist ** 2 / var_conns_on_pyr) / (np.sqrt(var_conns_on_pyr * 2 * np.pi))
#         if dist_normalizer > 0.01:
#             number_connections += 1
#         gmax_tmp += gmax * dist_normalizer
#
#     gmax = gmax_tmp
#     gmax_arr.append(gmax)
#
# plt.plot(grid_phases, gmax_arr)
# plt.show()
#
#
t = np.linspace(0, 3, 5000)

phis = 2*np.pi*0.5*t + 1.62
s = np.cos(phis)
plt.plot(t, s)
plt.show()

"""
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



I0 = bessel(kappa)

mu = 0
fi = np.linspace(-np.pi, np.pi, 1000, endpoint=True)
dfi = fi[1] - fi[0]
pdf = np.exp(kappa * np.cos(fi - mu) ) / (2 * np.pi * I0) 

print( np.sum(pdf) * dfi)
"""






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

    




