import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("../")
import presimulation_lib as prelib
from scipy.signal import argrelextrema

Nca3 = 100 #3500
Nmec = 100 #  3500

dt = 0.1
dur = 10000

pyr_center = 5000
tau_m = 20

Rtheta_ca3 = 0.3
Rtheta_mec = 0.3
Rgrid_mec = 0.9

t = np.arange(0, dur, dt)
theta_freq = 7.0 # Hz
theta_phases = 2 * np.pi * theta_freq * t * 0.001
theta_phases = theta_phases % (2 * np.pi)
theta_phases[theta_phases > np.pi] = theta_phases[theta_phases > np.pi] - 2 * np.pi


ca3_phase = 1.75
mec_phase = -1.75

place_t_radius = 500
var_conns_on_pyr = 9000

ca3_coord_x = np.cumsum( np.zeros(Nca3) + 200 ) # 200
mec_grid_phases = np.linspace(-np.pi, np.pi, Nmec)  # rad  !!!!!!!!!!!
mec_grid_freqs = np.zeros(Nmec) + 0.5


# ca3_gen_prob = []
# mec_gen_prob = []


pyr_leak = -np.arange(-5*tau_m, 0, dt) / tau_m


pyr_dynamics = 0


theta_kappa, theta_i0 = prelib.r2kappa(Rtheta_ca3)
for ca3_idx in range(Nca3):

    ca3_place = ca3_coord_x[ca3_idx]

    gen_prob = np.exp(theta_kappa * np.cos(theta_phases - ca3_phase)  ) / (2 * np.pi * theta_i0)
    gen_prob = gen_prob * np.exp( -0.5 * ((ca3_place - t) / place_t_radius)**2 )

    # gen_prob = gen_prob * np.exp(np.minimum(0, ca3_place-t ) / 300 )
    dist = ca3_place - pyr_center
    weight_dist = np.exp( -0.5 * dist**2 / var_conns_on_pyr  ) / (np.sqrt(var_conns_on_pyr * 2 * np.pi ) )
    # if dist > -200:
    #     weight_dist = weight_dist * 0.2

    pyr_dynamics += weight_dist * gen_prob # np.convolve(gen_prob, pyr_leak, mode="same")
    # ca3_gen_prob.append(gen_prob)
    # break



pyr_dynamics = pyr_dynamics / np.max(pyr_dynamics)

plt.plot(t, pyr_dynamics)



plt.show()

pyr_dynamics_ca3 = np.convolve(pyr_dynamics, pyr_leak, mode="same")


pyr_dynamics = 0

theta_kappa, theta_i0 = prelib.r2kappa(Rtheta_mec)
grid_kappa, grid_i0 = prelib.r2kappa(Rgrid_mec)

for mec_idx in range(Nmec):
    gen_prob = np.exp(theta_kappa * np.cos(theta_phases - mec_phase)) / (2 * np.pi * theta_i0)
    gen_prob *= np.exp(grid_kappa * np.cos(2*np.pi*t*0.001*mec_grid_freqs[mec_idx] + mec_grid_phases[mec_idx])) / (2 * np.pi * grid_i0)

    grid_freq = mec_grid_freqs[mec_idx]
    grid_phase = mec_grid_phases[mec_idx]
    #mec_gen_prob.append(gen_prob)
    grid_centers = 1000 * prelib.get_grid_centers(grid_freq, grid_phase, dur*0.001)

    # grid_phases = 2*np.pi*t*0.001*grid_freq
    # grid_phases = grid_phases % (2*np.pi)
    # grid_phases[grid_phases > np.pi] = grid_phases[grid_phases > np.pi] - (2*np.pi)
    #
    # gen_prob = gen_prob * np.exp(np.minimum(0, grid_phases-grid_phase ) / 0.8 )


    weight_dist = 0
    for cent in grid_centers:
        dist = cent - 500 - pyr_center
        dist_normalizer = np.exp(-0.5 * dist**2 / var_conns_on_pyr) / (np.sqrt(var_conns_on_pyr * 2 * np.pi))

        # if dist > 0:
        #     dist_normalizer = 0 #dist_normalizer * 0.2
        weight_dist += dist_normalizer

    pyr_dynamics += np.convolve(weight_dist * gen_prob, pyr_leak, mode="same") # weight_dist * gen_prob  #

pyr_dynamics = pyr_dynamics / np.max(pyr_dynamics)
pyr_dynamics_mec = np.convolve(pyr_dynamics, pyr_leak, mode="same")

pyr_dynamics = pyr_dynamics_ca3 + pyr_dynamics_mec

pyr_arg_peaks = argrelextrema(pyr_dynamics, np.greater)[0].astype(np.int)

# theta_phases
plt.figure()

plt.plot(t, pyr_dynamics_ca3)
plt.plot(t, pyr_dynamics_mec)
#

plt.figure()
plt.plot(t, pyr_dynamics)
plt.plot( t, np.max(pyr_dynamics) * np.cos(theta_phases) )
plt.scatter(t[pyr_arg_peaks], pyr_dynamics[pyr_arg_peaks], color="red")

plt.figure()
plt.scatter(t[pyr_arg_peaks], theta_phases[pyr_arg_peaks])
plt.ylim(-np.pi, np.pi)


plt.show()









