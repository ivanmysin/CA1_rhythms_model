import numpy as np
from neuron import h, load_mechanisms
import matplotlib.pyplot as plt
import os
import pandas as pd
from math import floor, log10
h.load_file("stdgui.hoc")
h.load_file("stdrun.hoc")

load_mechanisms("../mods/")

def f(number):
    if np.isnan(number):
        return " --- "
    if number == 0:
        return "0"
    is_negative = False
    if number < 0:
        is_negative = True
        number = -number
    sigfig = 2
    
    str_number = ("%.15f" % (round(number, int(-1 * floor(log10(number)) + (sigfig - 1))))).rstrip("0").rstrip(".")
    if is_negative:
        str_number = "-" + str_number
    return str_number

for cellfile in os.listdir("../cells/"):
    _, ext = os.path.splitext(cellfile)
    if ext != ".hoc": continue
    h.load_file("../cells/" + cellfile)

rem_param = ["e_ch_Navaxonp", "point_processes", "node_index", "na_ion", "sec", "v", "volume", "x", "ri", "k_ion", "ca_ion", "area", "ena", "ek"]


path2latextablefile = "/home/ivan/Документы/latex_supplement/" #pvbastable.tex"
celltype = "olm"

caption = "OLM cells parameters"
label = "ca1_" + celltype + "_cell_parameters"
# ca1_pyramidal_cell_parameters

path2latextablefile += celltype + "table.tex"

dend_pairs = []
dend_pairs.append(["dend 1", "dend 6", "dend 1"])
dend_pairs.append(["dend 2", "dend 7", "dend 2"])
dend_pairs.append(["dend 3", "dend 8", "dend 3"])
dend_pairs.append(["dend 4", "dend 9", "dend 4"])
dend_pairs.append(["dend 5", "dend 10", "dend 5"])
dend_pairs.append(["dend 11", "dend 14", "dend 6"])
dend_pairs.append(["dend 12", "dend 15", "dend 7"])
dend_pairs.append(["dend 13", "dend 16", "dend 8"])



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

            

pameters = sorted(list(set(pameters)))
try:
    pameters.remove("e_ch_Navaxonp")
except:
    pass

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
                    val = 1000 * val
                table.loc[param, name] = val
            if hasattr(seg, param):
                val = getattr(seg, param)
                if param.find("gmax") != -1:
                    val = 1000 * val
            
                table.loc[param, name] = val
        
        
# table = table.T.drop_duplicates(inplace=False).T
print(table) # = table
table.to_csv("this_cell.csv")


# for pair in dend_pairs:
#     table.drop(columns=pair[1], inplace=True)
#     table.rename(columns={ pair[0]: pair[2],}, inplace=True)

funsc = [f for _ in range(len(table.columns))] # len(table.index)
latex_lable = table.to_latex(na_rep=" --- ", longtable=True, caption=caption, label=label, formatters=funsc)

#  columns=["soma", ],


latex_lable = latex_lable.replace("Navaxonp", "Na")
# latex_lable = latex_lable.replace("e_", "E_")


latex_lable = latex_lable.replace(r"\_ch\_", "")
latex_lable = latex_lable.replace("cm", "$C, \\mu F / cm^2$")
latex_lable = latex_lable.replace("eleak", "$E_L,  mV$")
latex_lable = latex_lable.replace("gmaxleak", "$g_L,  mS / cm^2$")
latex_lable = latex_lable.replace("diam", "$D, \\mu m$")

latex_lable = latex_lable.replace("Ra", "$Ra,\n ohm \\cdot cm$")
latex_lable = latex_lable.replace("CavL", "CaL")
latex_lable = latex_lable.replace("CavN", "CaN")
latex_lable = latex_lable.replace("Nav", "Na")
latex_lable = latex_lable.replace("KvA", "KA")
latex_lable = latex_lable.replace("KvC", "KC")
latex_lable = latex_lable.replace("KvG", "KG")
latex_lable = latex_lable.replace("HCN", "H")
latex_lable = latex_lable.replace("eH", "$E_{H}, mV$")
latex_lable = latex_lable.replace("olm", "")
latex_lable = latex_lable.replace("ngf", "")
latex_lable = latex_lable.replace("cck", "")

latex_lable = latex_lable.replace("L               &", "$L, \\ \\mu m$ &")


latex_lable = latex_lable.replace("fast", "")

latex_lable_tmp = ""
for tmp_idx, tmp in enumerate (latex_lable.split("&")):
    if tmp.find("gmax") != -1:
        tmp = tmp.replace("gmax", "$g_{max, ")
        tmp += "}\\  mS / cm^2$" # \linebreak
    latex_lable_tmp += tmp + "&" 

latex_lable = latex_lable_tmp[:-1]


# old_str = "l" + "r" * len(table.columns)
# new_str = "p{.10\textwidth}" * (len(table.columns) + 1)
# \begin{longtable}{lrrrrrrrrrrrrrr}

# latex_lable = latex_lable.replace(old_str, new_str)
#latex_lable = latex_lable.replace("soma", "All compartments")


with open(path2latextablefile, "w") as texfile:
    texfile.write(latex_lable)
















