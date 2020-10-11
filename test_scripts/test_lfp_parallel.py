#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from mpi4py import MPI
from neuron import h, load_mechanisms
from neuron.units import ms, mV
h.nrnmpi_init()

from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.append("../")
sys.path.append("../../LFPsimpy/")
import presimulation_lib as prelib
from basic_parameters import basic_params as params
from LFPsimpy import LfpElectrode
from simulation_parallel import join_lfp

h.load_file("stdgui.hoc")
h.load_file("stdrun.hoc")
h.load_file("import3d.hoc")
h.cvode.use_fast_imem(1)

load_mechanisms("../mods/")
for cellfile in os.listdir("../cells/"):
    _, ext = os.path.splitext(cellfile)
    if ext != ".hoc": continue
    h.load_file("../cells/" + cellfile)

pc = h.ParallelContext()


postsynaptic_cell = "pyr"

cellclass = getattr(h, params["CellParameters"][postsynaptic_cell]["cellclass"])


all_cells = h.List()
pyramidal_sec_list = h.SectionList()
for idx in range(1):  # pc.id() +
    cell = cellclass(0, 0)
    
    for sec in cell.all:
        sec.insert("IextNoise")
        sec.myseed_IextNoise = np.random.randint(0, 1000000000000000, 1)
        sec.sigma_IextNoise = 0.005
        sec.mean_IextNoise = 0.005
        
        pyramidal_sec_list.append(sec)
    all_cells.append(cell)

radius_for_pyramids = 0.2
pyr_coord_in_layer_x = radius_for_pyramids * 2 * (np.random.rand() - 0.5) # density of the pyramidal cells  
pyr_coord_in_layer_y = radius_for_pyramids * 2 * (np.random.rand() - 0.5) # density of the pyramidal cells  
pyr_coord_in_layer_z =  np.random.normal(0, 20)
cell.position(pyr_coord_in_layer_x, pyr_coord_in_layer_z, pyr_coord_in_layer_y)
            
for sec in cell.all:
    sec.insert("IextNoise")
    
    sec.mean_IextNoise = params["CellParameters"][postsynaptic_cell]["iext"]
    sec.sigma_IextNoise = params["CellParameters"][postsynaptic_cell]["iext_std"]




generators = []
synapses = []
connections = []

tmp_params = deepcopy(params)

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
    "msach" : 3.14,
}

for pre_name, phase in cell_phases.items():
    
    
    
    connname = pre_name + "2" + postsynaptic_cell   
    

    
    try:
        conndata = tmp_params["connections"][connname]
    except KeyError:
        continue
    
    if pre_name == "pyr":
        conndata["prob"] *= 0.1

    print("Setting connection " + connname)
    gen_syns_conn = prelib.set_test_connections(h, conndata, pre_name, phase, cell, params)
    
    generators.extend(gen_syns_conn[0])
    synapses.extend(gen_syns_conn[1])
    connections.extend(gen_syns_conn[2])



Nelecs = params["Nelecs"]
el_x = np.zeros(Nelecs)
el_y = np.linspace(-200, 600, Nelecs)
el_z = np.zeros(Nelecs)


electrodes = []
for idx_el in range(Nelecs):
    le = LfpElectrode(x=el_x[idx_el], y=el_y[idx_el], z=el_z[idx_el], sampling_period=h.dt, sec_list=pyramidal_sec_list)
    electrodes.append(le)

h.tstop = 500 * ms # params["duration"]
pc.set_maxstep(10 * ms)
h.finitialize()

pc.barrier()
print("Start simulation")

pc.psolve(500 * ms) # params["duration"] 
# print("Time of simulation in sec ", time()-timer)
pc.barrier()
comm = MPI.COMM_WORLD

lfp_data = join_lfp(comm, electrodes)


if pc.id() == 0:
    fig, axes = plt.subplots( nrows=Nelecs, figsize=(15, 10))
    
    for key_idx, el in enumerate(electrodes):
                
        lfp = np.asarray(el.values)
        t = np.asarray(el.times)
        
        rem = t > 200
        lfp = lfp[rem]
        t = t[rem]
        
        
        
        axes[key_idx].plot(t, lfp, label=str(key_idx+1), color="blue" )
    
    
        axes[key_idx].legend()
                
                
            
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=0.4)
            
    plt.show()




