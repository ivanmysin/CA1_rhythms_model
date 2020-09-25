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
dur = 1000
Ncells = 100
celltype = "cckbas"


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
        sec.mean_IextNoise = RNG.normal(0.006, 0.002) # params["CellParameters"][celltype]["iext"]
        sec.sigma_IextNoise = params["CellParameters"][celltype]["iext_std"]

    cells.append(cell)

    firing = h.NetCon(cell.soma[0](0.5)._ref_v, None, sec=cell.soma[0])
    firing.threshold = -5 * mV

    fring_vector = h.Vector()
    firing.record(fring_vector)
    spike_count_obj.append(firing)
    spike_times_vecs.append(fring_vector)

connections = []
synapses = []

syn_params = params["connections"][celltype + "2" + celltype]
for pre_idx,  pre_cell in enumerate(cells):
    for post_idx,  post_cell in enumerate(cells):
        if pre_idx == post_idx: continue

        post_list = getattr(post_cell, syn_params["target_compartment"])
        len_postlist = sum([1 for _ in post_list])

        if len_postlist == 1:
            post_idx = 0
        else:
            post_idx = np.random.randint(0, len_postlist - 1)

        for idx_tmp, post_comp_tmp in enumerate(post_list):
            if idx_tmp == post_idx: post_comp = post_comp_tmp

        syn = h.Exp2Syn(post_comp(0.5))
        syn.e = syn_params["Erev"]
        syn.tau1 = syn_params["tau_rise"]
        syn.tau2 = syn_params["tau_decay"]

        conn = h.NetCon(pre_cell.soma[0](0.5)._ref_v, syn, sec=pre_cell.soma[0])
        conn.delay = syn_params["delay"]
        conn.weight[0] = syn_params["gmax"]

        connections.append(conn)
        synapses.append(syn)




h.tstop = dur
timer = time()
h.run()
print("Simulation time ", time() - timer)

fig, ax = plt.subplots()
for neuron_index, sp_train in enumerate(spike_times_vecs):
    sp_train = np.asarray(sp_train)
    indexes = np.zeros_like(sp_train) + 1 + neuron_index
    ax.scatter(sp_train, indexes, s=0.5, color="blue")

plt.show()




