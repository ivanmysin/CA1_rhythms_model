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

pre_pyr = h.CA1PyramidalCell(0, 0)
for sec in pre_pyr.all:
    sec.insert("IextNoise")
    sec.mean_IextNoise = 0.009
    sec.sigma_IextNoise = 0.001

post_pyr = h.CA1PyramidalCell(0, 0)

syn_ampa = h.Exp2Syn(post_pyr.soma[0](0.5))
syn_ampa.e = 0
syn_ampa.tau1 = 0.5
syn_ampa.tau2 = 3.0

conn = h.NetCon(pre_pyr.soma[0](0.5)._ref_v, syn_ampa, sec=pre_pyr.soma[0])
conn.delay = 0.5
conn.weight[0] = 0.009
conn.threshold = -30


syn_nmda = h.NMDA(post_pyr.soma[0](0.5), sec=post_pyr.soma[0])
syn_nmda.tcon = 2.4
syn_nmda.tcoff = 94.0
syn_nmda.gNMDAmax = 1.0 # 0.05

conn2 = h.NetCon(pre_pyr.soma[0](0.5)._ref_v, syn_nmda, sec=pre_pyr.soma[0])
conn2.delay = 0.5
conn2.weight[0] = 0.005 # * 0.01
conn2.threshold = -30

soma_v_pre = h.Vector()
soma_v_pre.record(pre_pyr.soma[0](0.5)._ref_v)

soma_v_post = h.Vector()
soma_v_post.record(post_pyr.soma[0](0.5)._ref_v)

I_nmda = h.Vector()
I_nmda.record(syn_nmda._ref_i)

t = h.Vector()
t.record(h._ref_t)

h.tstop = dur
h.run()

fig, ax = plt.subplots(nrows=3, sharex=True)
ax[0].plot(t, soma_v_pre)
ax[1].plot(t, soma_v_post)
ax[2].plot(t, I_nmda)

plt.show()






