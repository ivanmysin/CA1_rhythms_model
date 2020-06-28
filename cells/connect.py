import matplotlib.pyplot as plt
import numpy as np
import neuron
from neuron import h #, gui
h.load_file("stdgui.hoc")
h.load_file("import3d.hoc")
# h.nrn_load_dll("./mods/x86_64/.libs/libnrnmech.so")
neuron.load_mechanisms("../mods/")
h.load_file("class_pvbasketcell.hoc")
h.load_file("class_poolosyncell.hoc")

cell1 = h.poolosyncell(0, 0)
cell2 = h.pvbasketcell(0, 0)


stim1 = h.IClamp(0.5, sec=cell1.soma[0])
stim1.dur   = 100
stim1.delay = 0
stim1.amp = 0.8

# stim2 = h.IClamp(0.5, sec=cell2.soma[0])
# stim2.dur   = 100
# stim2.delay = 0
# stim2.amp = 0.8

soma1_v = h.Vector()
soma1_v.record(cell1.soma[0](0.5)._ref_v)

soma2_v = h.Vector()
soma2_v.record(cell2.soma[0](0.5)._ref_v)

syn = h.ExpSyn( 0.5, sec=cell2.soma[0])
syn.e = 0.0
syn.tau = 2.0




netcon = h.NetCon(cell1.soma[0](0.5)._ref_v, syn, sec=cell1.soma[0])
netcon.weight[0] = 0.01
netcon.delay = 0.5


t = h.Vector()
t.record(h._ref_t)

# run simulation
h.tstop = 100 # set the simulation time
h.run()

plt.plot(t, soma1_v, color="blue", linewidth = 5)
plt.plot(t, soma2_v, color="red")
plt.show()
