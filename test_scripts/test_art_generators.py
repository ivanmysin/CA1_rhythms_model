import numpy as np
from neuron import h, load_mechanisms
import matplotlib.pyplot as plt
import os
import sys
from copy import deepcopy

sys.path.append("../")
import presimulation_lib as prelib
from basic_parameters import get_object_params
from time import time
RNG = np.random.default_rng()
h.load_file("stdgui.hoc")
h.load_file("stdrun.hoc")

load_mechanisms("../mods/")

for cellfile in os.listdir("../cells/"):
    _, ext = os.path.splitext(cellfile)
    if ext != ".hoc": continue
    h.load_file("../cells/" + cellfile)


nthreads = 4

basic_params = get_object_params(nthreads)

params = basic_params[0]
###### parameters block ############
dur = 10000
Ngens = len(params["neurons"])
Rtheta = 0.3
Rgamma = 0.4

Rgrid = 0.9
#####################################




generators = []
firings = []
spike_times_vecs = []
places = np.cumsum( np.zeros(Ngens) + 150 ) #np.flip() #  np.flip( np.linspace(0, dur, Ngens) )

# print(places.size)

grid_phases = np.linspace(-np.pi, np.pi, Ngens)

for idx, neuron_param in enumerate(params["neurons"]):
    # theta_kappa, theta_i0 = prelib.r2kappa(Rtheta)
    # gamma_kappa, gamma_i0 = prelib.r2kappa(Rgamma)
    # grid_kappa, grid_i0 = prelib.r2kappa(Rgrid)

    # gen = h.ArtificialRhytmicPlaceCell()
    #gen = h.ArtificialRhytmicGridCell()
    #gen.delta_t = 0.1

    # gen.spike_rate = 1000000
    # gen.place_center_t = places[idx]
    # gen.place_t_radius = 500
    #gen.grid_freqs = 1.5
    #gen.grid_kappa = grid_kappa
    #gen.grid_I0 = grid_i0
    #gen.grid_phase = 1.5 # grid_phases[idx]
    celltypename = neuron_param["celltype"]
    cellclass_name = neuron_param["cellclass"]
    gid = neuron_param["gid"]

    cellclass = getattr(h, cellclass_name)

    cell = cellclass(gid, 0)
    
    # gen.latency = 10
    #
    # gen.low_kappa = theta_kappa
    # gen.low_I0 = theta_i0
    # gen.high_kappa = gamma_kappa
    # gen.high_I0 = gamma_i0

    for p_name, p_val in neuron_param["cellparams"].items():
        if hasattr(cell.acell, p_name):
            setattr(cell.acell, p_name, p_val)
    setattr(cell.acell, "myseed", RNG.integers(0, 1000000000000000, 1))


    firing = h.NetCon(cell.acell, None)
    fring_vector = h.Vector()
    
    firing.record(fring_vector)
    
    
    generators.append(cell)
    firings.append(firing)
    spike_times_vecs.append(fring_vector)

print(idx)

h.tstop = dur
h.run()


fig, ax = plt.subplots(nrows=1, sharex=True)
for idx in range(len(spike_times_vecs)):
    
    t = np.asarray( spike_times_vecs[idx] )

    #print(t.size)

    fir = np.zeros_like(t) + idx + 1
    ax.scatter(t, fir, color="blue", s=0.5)
    

    
    #a = np.cos(phis) + 1j*np.sin(phis)

    #angle = np.angle(np.sum(a))
    #print(angle)


# tcentrs = 1000 * prelib.get_grid_centers(1.5, 1.5, dur*0.001)
#
# t = np.arange(0, dur, 0.2) # np.linspace(0, dur, 10000)
# phi = 2*np.pi * 5 * 0.001 * t #- 1.5
#
# s = np.cos(phi)  #np.cos(2*np.pi*grid_w*tgrid + grid_phase) )
#
#
#
# ax[0].plot(t, s, color="blue")
# ax[0].plot(t, np.zeros_like(t), color="green")
# ax[0].scatter(tcentrs, np.zeros_like(tcentrs), color="red")



ax.set_ylim(0, len(spike_times_vecs))
plt.show()
