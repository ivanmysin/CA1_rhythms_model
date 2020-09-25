import numpy as np
import sys
import matplotlib.pyplot as plt 
sys.path.append("../")
import presimulation_lib as lib
rng = np.random.default_rng()



# CA3 place cell artificial generator
dt = 0.005
dur = 5
Ngens = 100


theta_w = 5
theta_phase_mean = 1.5
Rteta = 0.6
theta_kappa, theta_i0 = lib.r2kappa(Rteta)


gamma_w = 30
gamma_phase_mean = 0
Rgamma = 0.6
gamma_kappa, gamma_i0 = lib.r2kappa(Rgamma)

place_cent_t = np.flip( np.linspace(0, dur, Ngens) )
place_radius = 1.0




firing_t = np.empty(0, dtype=np.float)
firing_n = np.empty_like(firing_t)
n_indxes = np.arange(1, Ngens+1, 1)

theta_phase = 0
gamma_phase = 0

dfi_theta = dt * theta_w
dfi_gamma = dt * gamma_w


for t in np.arange(0, dur, dt):
    generators = rng.random(Ngens)

    pdf_theta = np.exp(theta_kappa * np.cos(theta_phase - theta_phase_mean) ) / (2 * np.pi * theta_i0)
    pdf_gamma = np.exp(gamma_kappa * np.cos(gamma_phase - gamma_phase_mean) ) / (2 * np.pi * gamma_i0)

    pdf_place = np.exp( -0.5 * ( (t - place_cent_t) / place_radius)**2 ) / (place_radius * np.sqrt(2*np.pi) )

    pdf = dfi_gamma * pdf_gamma * pdf_theta * dfi_theta * 500 * pdf_place

    fired = generators < pdf
    firing_n = np.append(firing_n, n_indxes[fired] )
    firing_t = np.append(firing_t, np.zeros(np.sum(fired)) + t)





    theta_phase += dfi_theta
    gamma_phase += dfi_gamma


plt.scatter(firing_t, firing_n, s=0.5)
plt.show()



