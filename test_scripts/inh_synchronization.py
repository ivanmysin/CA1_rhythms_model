import numpy as np
from neuron import h, load_mechanisms
from neuron.units import ms, mV

import matplotlib.pyplot as plt
import os
import sys
from copy import deepcopy

sys.path.append("../")
import presimulation_lib as prelib
from basic_parameters import basic_params
from time import time
###### parameters block ############
dur = 100
Ncells = 100
celltype = "pvbas"


params = deepcopy(basic_params)
#####################################

RNG = np.random.default_rng()
h.load_file("stdgui.hoc")
h.load_file("stdrun.hoc")

load_mechanisms("../mods/")

for cellfile in os.listdir("../cells/"):
    _, ext = os.path.splitext(cellfile)
    if ext != ".hoc": continue
    h.load_file("../cells/" + cellfile)


cellclass = getattr(h, params["CellParameters"][celltype]["cellclass"])

cells = []
spike_count_obj = []
spike_times_vecs = []
for idx in range(Ncells):
    cell = cellclass(idx, 0)

    for sec in cell.all:
        sec.insert("IextNoise")
        sec.mean_IextNoise = 0.006 # params["CellParameters"][celltype]["iext"]
        sec.sigma_IextNoise = params["CellParameters"][celltype]["iext_std"]

    cells.append(cell)

    firing = h.NetCon(cell.soma[0](0.5)._ref_v, None, sec=cell.soma[0])
    firing.threshold = -5 * mV

    fring_vector = h.Vector()
    firing.record(fring_vector)
    spike_count_obj.append(firing)
    spike_times_vecs.append(fring_vector)






h.tstop = dur
timer = time()
h.run()
print("Simulation time ", time() - timer)

fig, ax = plt.subplots()
for neuron_index, sp_train in enumerate(spike_times_vecs):
    sp_train = np.asarray(sp_train)
    indexes = np.zeros_like(sp_train) + 1 + neuron_index
    ax.scatter(sp_train, indexes)

plt.show()




