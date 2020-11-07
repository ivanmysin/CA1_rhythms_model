import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import vonmises
import h5py
import sys
sys.path.append("../")
import presimulation_lib as lib

def generate_firing(theta_w, gamma_w, theta_phase_mean, gamma_phase_mean, Ngens, Rtheta, Rgamma, dur):
    rng = np.random.default_rng()

    dur *= 1000
    dt = 0.1
    dfi_theta = dt * 0.001 * theta_w * 2 * np.pi
    dfi_gamma = dt * 0.001 * gamma_w * 2 * np.pi

    theta_kappa, theta_i0 = lib.r2kappa(Rtheta)
    gamma_kappa, gamma_i0 = lib.r2kappa(Rgamma)
    
    theta_phase = 0
    gamma_phase = 0
    
    firing_t = np.empty(0, dtype=np.float)
    firing_n = np.empty_like(firing_t)
    n_indxes = np.arange(1, Ngens+1, 1)
    
    for t in np.arange(0, dur, dt):
        generators = rng.random(Ngens)

        pdf_theta = np.exp(theta_kappa * np.cos(theta_phase - theta_phase_mean) ) / (2 * np.pi * theta_i0)
        pdf_gamma = np.exp(gamma_kappa * np.cos(gamma_phase - gamma_phase_mean) ) / (2 * np.pi * gamma_i0)

        pdf = dfi_gamma * pdf_gamma * pdf_theta * dfi_theta * 1000

        theta_phase += dfi_theta
        gamma_phase += dfi_gamma

        fired = generators < pdf
        firing_n = np.append(firing_n, n_indxes[fired] )
        firing_t = np.append(firing_t, np.zeros(np.sum(fired)) + t)
    
    return firing_n, firing_t






RESULTFILE = "../../../Data/CA1_simulation/artificial_signals.hdf5"
duration = 1
sampling_rate = 10000
t = np.linspace(0, duration, duration*sampling_rate)
theta_w = 8
theta_phases = 2*np.pi*t*theta_w

kappa = 5.2
gamma_w = 32
slow_gamma_phases = 2*np.pi*t*gamma_w
fast_gamma_phases = 2*np.pi*t*72



lfp = np.cos(theta_phases) 
lfp += 0.8*vonmises.pdf(theta_phases, kappa, loc=1.5, scale=1)*np.cos(slow_gamma_phases)
lfp += 0.7*vonmises.pdf(theta_phases, kappa, loc=np.pi, scale=1)*np.cos(fast_gamma_phases)
lfp += np.random.normal(0, 0.05, lfp.size)


cell_phases = {
    # "ca3"    : 1.5,
    # "mec"    : 0.0,
    # "lec"    : 0.0,
    "pvbas"  : 1.5,
    "olm"    : 3.14,
    "cckbas" : -1.5,
    "aac"    : 0.0,
    "bis"    : 3.14,
    "ivy"    : -2.63,
    "ngf"    : 0.0,
    "pyr"    : 3.14,
    # "msteevracells" : 3.14,
    # "mskomalicells" : 0.0,
    # "msach" : 3.14,
}


firing_celltypes = {}
Ngens = 100
for celltype, theta_phase_mean in cell_phases.items():
    
    print(theta_phase_mean)
    gamma_phase_mean = 0
    Rtheta = 0.4
    Rgamma = 0.6
    firing_index, firing_times = generate_firing(theta_w, gamma_w, theta_phase_mean, gamma_phase_mean, Ngens, Rtheta, Rgamma, duration)

    # plt.scatter(firing_times, firing_index)
    # plt.show()

    firing_celltypes[celltype] = []
    for idx in np.unique(firing_index):
        sp_times = firing_times[firing_index == idx]
        firing_celltypes[celltype].append(sp_times)



with h5py.File(RESULTFILE, 'w') as h5file:
    
    h5file.create_dataset("time", data = t*1000)
    
    extracellular_group = h5file.create_group("extracellular")
    ele_group = extracellular_group.create_group('electrode_1')
    lfp_group = ele_group.create_group('lfp')
           
    lfp_group_origin = lfp_group.create_group('origin_data')
    lfp_group_origin.attrs['SamplingRate'] = sampling_rate
    
    lfp_group_origin.create_dataset("channel_1", data=lfp)
    # lfp_group_origin.create_dataset("channel_2", data=lfp)
    # lfp_group_origin.create_dataset("channel_3", data=lfp)

    firing_group = h5file.create_group("extracellular/electrode_1/firing/origin_data")



    for celltype, spike_trains in firing_celltypes.items():
        cell_friring_group = firing_group.create_group(celltype)
        for cell_idx, sp_times in enumerate(spike_trains):
            cell_friring_group.create_dataset("neuron_" + str(cell_idx+1), data=sp_times) 













plt.plot(t, lfp)
plt.show()
