import numpy as np
from neuron import h, load_mechanisms
from neuron.units import ms, mV

import matplotlib.pyplot as plt
import os
import sys
from copy import deepcopy

sys.path.append("../")
import presimulation_lib as prelib
# from basic_parameters import basic_params
from time import time

RNG = np.random.default_rng()
h.load_file("stdgui.hoc")
h.load_file("stdrun.hoc")

load_mechanisms("../mods/")

for cellfile in os.listdir("../cells/"):
    _, ext = os.path.splitext(cellfile)
    if ext != ".hoc": continue
    h.load_file("../cells/" + cellfile)
###### parameters block ############
dur = 3000
Nca3 = 50
Nmec = 50
Npyr = 20

Rtheta = 0.2
Rgamma = 0.4

theta_kappa, theta_I0 = prelib.r2kappa(Rtheta)
gamma_kappa, gamma_I0 = prelib.r2kappa(Rgamma)

####################################
cells = []
spike_count_obj = []
spike_times_vecs = []

connections = []
synapses = []

for pyr_idx in range(Npyr):

    cell = h.CA1PyramidalCell(0, 0)

    for sec in cell.all:
        sec.insert("IextNoise")
        sec.mean_IextNoise = 0
        sec.sigma_IextNoise = 0.002

    cells.append(cell)

firing = h.NetCon(cell.soma[0](0.5)._ref_v, None, sec=cell.soma[0])
firing.threshold = -5 * mV
fring_vector = h.Vector()
firing.record(fring_vector)
spike_count_obj.append(firing)
spike_times_vecs.append(fring_vector)


for idx in range(Nca3 + Nmec):
    cell = h.ArtifitialPlaceCell(0, 0)
    
    if idx >= Nca3:
        # mec
        cell.acell.low_mu = np.deg2rad(100)
        cell.acell.place_center_t = 1000
        gmax = 0.005
        
        post_comp_name = "lm_list"
        
    else:
        # ca3
        cell.acell.low_mu = np.deg2rad(260)
        cell.acell.place_center_t = 1300
        gmax = 0.005
        
        post_comp_name = "rad_list"
    
    post_list = getattr(cells[0], post_comp_name)
    len_postlist = sum([1 for _ in post_list])
        
    if len_postlist == 1:
        post_idx = 0
    else:
        post_idx = RNG.integers(0, len_postlist-1)

    for idx_tmp, post_comp_tmp in enumerate(post_list):
        if idx_tmp == post_idx: post_comp = post_comp_tmp
    
    cell.acell.high_mu = 0
    cell.acell.place_t_radius = 500

    cell.acell.low_kappa = theta_kappa
    cell.acell.low_I0 = theta_I0
    cell.acell.high_kappa = gamma_kappa
    cell.acell.high_I0 = gamma_I0
    cell.acell.spike_rate = 500000 # 100000
    cell.acell.latency = 10
    cell.acell.delta_t = 0.2

    cell.acell.myseed = RNG.integers(0, 1000000000, 1)

    firing = h.NetCon(cell.acell, None)
    fring_vector = h.Vector()
    firing.record(fring_vector)
    
    spike_count_obj.append(firing)
    spike_times_vecs.append(fring_vector)
    
    
    syn = h.Exp2Syn(post_comp(0.5))
    syn.e = 0
    syn.tau1 = 0.5
    syn.tau2 = 3.0

    conn = h.NetCon(cell.acell, syn, sec=post_comp)
    conn.delay = 10
    conn.weight[0] = gmax

    
    cells.append(cell)
    connections.append(conn)
    synapses.append(syn)


print("Start simulation")
h.tstop = dur
timer = time()
h.run()
print("Simulation time ", time() - timer)
print(len(spike_times_vecs))

fig, ax = plt.subplots(nrows=2)
for neuron_index, sp_train in enumerate(spike_times_vecs):
    sp_train = np.asarray(sp_train)
    indexes = np.zeros_like(sp_train) + 1 + neuron_index
    
    if neuron_index == 0:
        t = np.linspace(0, dur, 10000)
        ax[0].plot(t, np.cos(2*np.pi*t*0.005) )
        ax[0].scatter(sp_train, indexes, s=2, color="red")
    else:
        # print(sp_train.size)
        ax[1].scatter(sp_train, indexes, s=0.5, color="blue")


fig, ax = plt.subplots(nrows=1)
for pyr_idx in range(Npyr):

    sp_train = spike_times_vecs[pyr_idx]
    sp_train = np.asarray(sp_train)

    theta_phases = 2*np.pi*sp_train*0.005
    theta_phases = theta_phases % (2*np.pi)
    theta_phases[theta_phases > np.pi] = theta_phases[theta_phases > np.pi] - 2*np.pi
    ax.scatter(sp_train, theta_phases, s=2, color="green")

plt.show()
