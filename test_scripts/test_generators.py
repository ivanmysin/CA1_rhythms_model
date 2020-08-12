import numpy as np
from neuron import h, load_mechanisms
import matplotlib.pyplot as plt
import os
import sys

sys.path.append("../")
import presimulation_lib as prelib


###### parameters block ############

dur = 1500
delay_mean = np.log(1)
delay_sigma = 0.5

gmax_mean = np.log(0.001)
gmax_sigma = 0.5

Rgens = 0.6  # Ray length of generators
kappa, I0 = prelib.r2kappa(Rgens)


#####################################

RNG = np.random.default_rng()
h.load_file("stdgui.hoc")
h.load_file("stdrun.hoc")

load_mechanisms("../mods/")

for cellfile in os.listdir("../cells/"):
    _, ext = os.path.splitext(cellfile)
    if ext != ".hoc": continue
    h.load_file("../cells/" + cellfile)
       


cell = h.poolosyncell(0, 0)

for sec in cell.all:
    sec.insert("IextNoise")
    sec.sigma_IextNoise = 0.005
    sec.mean_IextNoise = 0.0


post_comp = cell.soma[0]
generators = []
synapses = []
connections = []

len_radlist = sum([1 for _ in cell.rad_list])

for idx in range(100):
    
    post_idx = np.random.randint(0, len_radlist-1)
    
    for idx, post_comp in enumerate(cell.rad_list):
        if idx == post_idx: break
    
    
    gen = h.ArtifitialCell(0, 0)
    gen.acell.mu = np.pi
    gen.acell.latency = 1
    gen.acell.freqs = 5
    gen.acell.spike_rate = 5
    gen.acell.kappa = kappa
    gen.acell.I0 = I0

    syn = h.Exp2Syn( post_comp(0.5) ) 
    syn.e = 0       #  conn_data["Erev"]
    syn.tau1 = 0.5  # conn_data["tau_rise"]
    syn.tau2 = 2.5  # conn_data["tau_decay"]
    
    conn = h.NetCon(gen.acell, syn, sec=post_comp)
            
    conn.delay = RNG.lognormal(delay_mean, delay_sigma)    # np.random.lognormal(mean=np.log(conn_data["delay"]), sigma=conn_data["delay_std"])   
    conn.weight[0] = RNG.lognormal(gmax_mean, gmax_sigma)  # conn_data["gmax"] 
    
    
    generators.append(gen)
    synapses.append(syn)
    connections.append(conn)





t = h.Vector()
t.record(h._ref_t)


soma_v = h.Vector()
soma_v.record(cell.soma[0](0.5)._ref_v)

h.tstop = dur
h.run()


plt.plot(t, soma_v)
plt.show()






