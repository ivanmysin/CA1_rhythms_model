import numpy as np
from neuron import h, load_mechanisms
import matplotlib.pyplot as plt
import os
import sys
from copy import deepcopy

sys.path.append("../")
import presimulation_lib as prelib
from basic_parameters import basic_params


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


postsynaptic_cell = "aac"

cellclass = getattr(h, basic_params["CellParameters"][postsynaptic_cell]["cellclass"])
cell = cellclass(0, 0)



for sec in cell.all:
    sec.insert("IextNoise")
    
    sec.mean_IextNoise = basic_params["CellParameters"][postsynaptic_cell]["iext"]
    sec.sigma_IextNoise = basic_params["CellParameters"][postsynaptic_cell]["iext_std"]




generators = []
synapses = []
connections = []

params = deepcopy(basic_params)

cell_phases = {
    "ca3"    : 1.5,
    "mec"    : 0.0,
    "lec"    : 0.0,
    "pvbas"  : 1.5,
    "olm"    : 3.14,
    "cckbas" : -1.5,
    "aac"    : 0.0,
    "bis"    : 3.14,
    "ivy"    : -2.63,
    "ngf"    : 0.0,
    "pyr"    : 3.14,
    "msteevracells" : 3.14,
    "mskomalicells" : 0.0,
}

for pre_name, phase in cell_phases.items():
    
    
    
    connname = pre_name + "2" + postsynaptic_cell   
    

    
    try:
        conndata = params["connections"][connname]
    except KeyError:
        continue
    
    if pre_name == "pyr":
        conndata["prob"] *= 0.1

    print("Setting connection " + connname)
    gen_syns_conn = prelib.set_test_connections(h, conndata, pre_name, phase, cell, params)
    
    generators.extend(gen_syns_conn[0])
    synapses.extend(gen_syns_conn[1])
    connections.extend(gen_syns_conn[2])
    
    



t = h.Vector()
t.record(h._ref_t)


soma_v = h.Vector()
soma_v.record(cell.soma[0](0.5)._ref_v)

h.tstop = dur
h.run()

t = np.asarray(t)

theta_rhythm = 20 * np.cos(2 * np.pi * 0.005 * t)

plt.plot(t, soma_v, color="blue")
plt.plot(t, theta_rhythm, color="red")
plt.show()






