import numpy as np
from neuron import h, load_mechanisms
import matplotlib.pyplot as plt
import os
import sys

sys.path.append("../")
import presimulation_lib as prelib
from basic_parameters import basic_params


###### parameters block ############
dur = 1500

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



generators = []
synapses = []
connections = []



# connections from ca3 to pyramids
conndata = basic_params["connections"]["ca32pyr"]
pre_name = "ca3"
post_name = "rad_list"
phase = 1.5
gen_syns_conn = prelib.set_test_connections(h, conndata, pre_name, phase, cell, basic_params)

generators.extend(gen_syns_conn[0])
synapses.extend(gen_syns_conn[1])
connections.extend(gen_syns_conn[2]) 



# connections from mec to pyramids
conndata = basic_params["connections"]["mec2pyr"]
pre_name = "mec"
phase = 0.0
gen_syns_conn = prelib.set_test_connections(h, conndata, pre_name, phase, cell, basic_params)

generators.extend(gen_syns_conn[0])
synapses.extend(gen_syns_conn[1])
connections.extend(gen_syns_conn[2]) 


# connections from pvbas to pyramids
conndata = basic_params["connections"]["pvbas2pyr"]
pre_name = "pvbas"
phase = 1.5
gen_syns_conn = prelib.set_test_connections(h, conndata, pre_name, phase, cell, basic_params)

generators.extend(gen_syns_conn[0])
synapses.extend(gen_syns_conn[1])
connections.extend(gen_syns_conn[2]) 


# connections from cckbas to pyramids
conndata = basic_params["connections"]["cckbas2pyr"]
pre_name = "cckbas"
phase = -1.5
gen_syns_conn = prelib.set_test_connections(h, conndata, pre_name, phase, cell, basic_params)

generators.extend(gen_syns_conn[0])
synapses.extend(gen_syns_conn[1])
connections.extend(gen_syns_conn[2]) 


# connections from olm to pyramids
conndata = basic_params["connections"]["olm2pyr"]
pre_name = "olm"
phase = 3.14
gen_syns_conn = prelib.set_test_connections(h, conndata, pre_name, phase, cell, basic_params)

generators.extend(gen_syns_conn[0])
synapses.extend(gen_syns_conn[1])
connections.extend(gen_syns_conn[2]) 


# connections from axo to pyramids
conndata = basic_params["connections"]["axo2pyr"]
pre_name = "axo"
phase = 0.0   # !!!!!!!
gen_syns_conn = prelib.set_test_connections(h, conndata, pre_name, phase, cell, basic_params)

generators.extend(gen_syns_conn[0])
synapses.extend(gen_syns_conn[1])
connections.extend(gen_syns_conn[2]) 


# connections from ivy to pyramids
conndata = basic_params["connections"]["ivy2pyr"]
pre_name = "ivy"
phase = -2.63   # !!!!!!!
gen_syns_conn = prelib.set_test_connections(h, conndata, pre_name, phase, cell, basic_params)

generators.extend(gen_syns_conn[0])
synapses.extend(gen_syns_conn[1])
connections.extend(gen_syns_conn[2]) 


# connections from ngf to pyramids
conndata = basic_params["connections"]["ngf2pyr"]
pre_name = "ngf"
phase = 0.0   # !!!!!!!
gen_syns_conn = prelib.set_test_connections(h, conndata, pre_name, phase, cell, basic_params)

generators.extend(gen_syns_conn[0])
synapses.extend(gen_syns_conn[1])
connections.extend(gen_syns_conn[2]) 


# connections from bis to pyramids
conndata = basic_params["connections"]["bis2pyr"]
pre_name = "bis"
phase = 3.14   # !!!!!!!
gen_syns_conn = prelib.set_test_connections(h, conndata, pre_name, phase, cell, basic_params)

generators.extend(gen_syns_conn[0])
synapses.extend(gen_syns_conn[1])
connections.extend(gen_syns_conn[2]) 




t = h.Vector()
t.record(h._ref_t)


soma_v = h.Vector()
soma_v.record(cell.soma[0](0.5)._ref_v)

h.tstop = dur
h.run()


plt.plot(t, soma_v)
plt.show()






