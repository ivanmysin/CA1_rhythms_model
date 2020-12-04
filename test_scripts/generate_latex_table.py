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


path2latextablefile = "/home/ivan/Документы/latex_supplement/pvbastable.tex"
celltype = "pvbas"

cells_params = {
        "pyr" : {
            "cellclass" : "CA1PyramidalCell", # "poolosyncell", # 
            "iext" : 0.0, # 0.002,
            "iext_std" : 0.002,
        },
        
        "pvbas" : {
            "cellclass" : "pvbasketcell",
            "iext" : 0.0,
            "iext_std" : 0.0,
        },
        
        "cckbas" : {
            "cellclass" : "cckcell",
            "iext" : 0.002, #!!! 0.003,
            "iext_std" : 0.004,
        },

        "olm" : {
            "cellclass" : "olmcell",
            "iext" : 0.0,
            "iext_std" : 0.002,
        },
        
        "aac" : {
            "cellclass" : "axoaxoniccell",
            "iext" : 0.0,
            "iext_std" : 0.002,
        },
        
        "ngf" : {
            "cellclass" : "ngfcell",
            "iext" : 0.002,
            "iext_std" : 0.002,
        },
        
        "ivy" : {
            "cellclass" : "ivycell",
            "iext" : 0.002,
            "iext_std" : 0.002,
        },
    
        "bis" : {
            "cellclass" : "CA1BistratifiedCell", # "bistratifiedcell",
            "iext" : 0.005,
            "iext_std" : 0.002,
        },
        
        "sca" : {
            "cellclass" : "scacell",
            "iext" : 0.001,
            "iext_std" : 0.002,
        },
    
}


cellclass = getattr(h, cells_params[celltype]["cellclass"]  )
cell = cellclass(0, 0)

names = [] # "Parameter", 
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


pameters = ["L", "Ra"]



for sec_idx, sec in enumerate(cell.all):
    assert (sec.name() == scr_names[sec_idx])

    name = names[sec_idx]
    
    
    for seg in sec:
        mechs = dir(seg)
        
        for mech in mechs:
            if mech[0:2] == "__" or mech in rem_param: continue
           
            if hasattr(seg, "gmax_" + mech):
                param = "gmax_" + mech
                pameters.append(param)
            
            if hasattr(seg,  "e_" + mech):
                param = "e_" + mech
                pameters.append(param)
            
            if hasattr(sec, mech):
                param = mech
                pameters.append(param)

            

pameters = list(set(pameters))
# print(pameters)
table = pd.DataFrame(np.nan, index=pameters, columns=names) 
table.index.name = "Parameters"

for sec_idx, sec in enumerate(cell.all):
    assert (sec.name() == scr_names[sec_idx])

    name = names[sec_idx]
    
    for seg in sec:
        for param in pameters:
            if hasattr(sec, param):
                val = getattr(sec, param)
                if param.find("gmax") != -1:
                    val *= 1000
            if hasattr(seg, param):
                val = getattr(seg, param)
            
            table.loc[param, name] = val
        
        
# table = table.T.drop_duplicates(inplace=False).T
print(table) # = table


latex_lable = table.to_latex(na_rep=" --- ", float_format="%.5f", longtable=True)


latex_lable = latex_lable.replace(r"\_ch\_", "")
latex_lable = latex_lable.replace("cm", "C, $\\mu F / cm^2$")
latex_lable = latex_lable.replace("eleak", "$E_L, mV$")
latex_lable = latex_lable.replace("diam", "D, $\\mu m$")
latex_lable = latex_lable.replace("\\\\\nL", "\\\\\nL, $\\mu m$")
latex_lable = latex_lable.replace("Ra", "Ra, $ohm cm$")
latex_lable = latex_lable.replace("CavL", "CaL")
latex_lable = latex_lable.replace("CavN", "CaN")
latex_lable = latex_lable.replace("Nav", "Na")
latex_lable = latex_lable.replace("KvA", "KA")
latex_lable = latex_lable.replace("KvC", "KC")

latex_lable = latex_lable.replace("fast", "")
latex_lable = latex_lable.replace("gmax", "$g_{max, }$")


with open(path2latextablefile, "w") as texfile:
    texfile.write(latex_lable)
















