import numpy as np
from neuron import h, load_mechanisms
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

#####################################

RNG = np.random.default_rng()
h.load_file("stdgui.hoc")
h.load_file("stdrun.hoc")

load_mechanisms("../mods/")


for cellfile in os.listdir("../cells/"):
    _, ext = os.path.splitext(cellfile)
    if ext != ".hoc": continue
    h.load_file("../cells/" + cellfile)

cell1 = h.pvbasketcell(0, 0)
for sec in cell1.all:
    sec.insert("IextNoise")
    sec.mean_IextNoise = 0.003
    sec.sigma_IextNoise = 0.001


cell2 = h.pvbasketcell(1, 1)
gap = h.GAP(cell2.soma[0](0.5), sec=cell2.soma[0])
gap.r = 100000
h.setpointer(cell1.soma[0](0.5)._ref_v, 'vgap', gap)

soma_v_pre = h.Vector()
soma_v_pre.record(cell1.soma[0](0.5)._ref_v)

soma_v_post = h.Vector()
soma_v_post.record(cell2.soma[0](0.5)._ref_v)


t = h.Vector()
t.record(h._ref_t)

h.tstop = dur
h.run()

fig, ax = plt.subplots(nrows=2, sharex=True)
ax[0].plot(t, soma_v_pre)
ax[1].plot(t, soma_v_post)


plt.show()

