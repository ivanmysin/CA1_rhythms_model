import numpy as np
from neuron import h, load_mechanisms
import matplotlib.pyplot as plt
import os
import pandas as pd

h.load_file("stdgui.hoc")
h.load_file("stdrun.hoc")

load_mechanisms("../mods/")

for cellfile in os.listdir("../cells/"):
    _, ext = os.path.splitext(cellfile)
    if ext != ".hoc": continue
    h.load_file("../cells/" + cellfile)

rem_param = ["point_processes", "node_index", "na_ion", "sec", "v", "volume", "x", "ri", "k_ion", "ca_ion", "area"]



postsynaptic_cell = "pvbas"

cellclass = getattr(h, "pvbasketcell")
cell = cellclass(0, 0)

names = ["Parameter", ]
scr_names = []
for sec in cell.all:

    name = sec.name()
    scr_names.append(name)
    
    name = name.split(".")[-1]
    name = name.replace("]", "")
    
    name, number = name.split("[")
    if not (name == "soma" or name =="axon"):
        number = int(number) + 1
        name = name + " " + str(number)
    # print(name)
    
    
    names.append(name)

    

table = pd.DataFrame(columns=names)

pameters = ["L", "Ra"]



for sec_idx, sec in enumerate(cell.all):
    assert (sec.name() == scr_names[sec_idx])
    
    # print(sec.L)
    # print(sec.Ra)
    name = names[sec_idx + 1]
    
    
    for seg in sec:
        mechs = dir(seg)
        
        for mech in mechs:
            if mech[0:2] == "__" or mech in rem_param: continue
            
            try:
                att = "gmax_" + mech
                print( getattr(sec,  att) )
            
            except AttributeError:
                print(  getattr(seg,  mech) )
            
            
            
            

    break
    

# table.append( pd.Series(), ignore_index=True )
    
#print(table)















