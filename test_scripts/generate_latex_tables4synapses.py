import pandas as pd

import sys
sys.path.append("../")
from basic_parameters import get_basic_params

PATH4TABLES = "/home/ivan/Документы/latex_supplement/"

params = get_basic_params()
celltypes = sorted( list(set([neuron for neuron in params["CellParameters"].keys()])) )
synapse_params = [p for p in params["gap_junctions_params"]["pvbas2pvbas"].keys()]

try:
    synapse_params.remove("sourse_compartment")
except:
    pass
try:
    synapse_params.remove("NMDA")
except:
    pass

try:
    synapse_params.remove("Erev")
except:
    pass
try:
    synapse_params.remove("compartment2")
except:
    pass
code4insertion = ""

for celltype in celltypes:
    print(celltype)
    table = pd.DataFrame(data=None, index=celltypes, columns=synapse_params)
    
    for conname, conndata in params["gap_junctions_params"].items():
        precell, postcell = conname.split("2")
        if postcell != celltype: continue
        
        #print(precell)
        for syn_param in synapse_params:
            table.loc[precell, syn_param] = conndata[syn_param]

    table.dropna(inplace=True)
    if len(table) == 0:
        print(celltype)
        continue
    
    table = table.rename( columns={"r":"Rmean"} )
    
    print(table)
    table_file = celltype + "_gap_junctions.tex"
    code4insertion += r"\input{" + table_file + "}\n"
    
    caption = "Gap junctions between " + celltype
    caption = caption.replace("_", "\\_")

    label = celltype + "_gap"
    latex_lable = table.to_latex(na_rep=" --- ", longtable=True, label=label, caption=caption)
    latex_lable = latex_lable.replace("gmax\\_std", "$g_{max, \sigma}$")
    latex_lable = latex_lable.replace("gmax", "$g_{max, mean}$")
    latex_lable = latex_lable.replace("tau\\_rise", "$\\tau_{rise}$")
    latex_lable = latex_lable.replace("tau\\_decay", "$\\tau_{decay}$")
    latex_lable = latex_lable.replace("delay\\_std", "$de!lay_{\sigma}$")
    latex_lable = latex_lable.replace("delay", "$delay_{mean}$")
    latex_lable = latex_lable.replace("!", "")
    latex_lable = latex_lable.replace("_list", "")
    latex_lable = latex_lable.replace("target\\_compartment", "Compartment")
    latex_lable = latex_lable.replace("compartment1", "Compartment")
    latex_lable = latex_lable.replace("prob", "$p$")
    latex_lable = latex_lable.replace("r\\_std", "$R_{gap, \sigma}$")
    latex_lable = latex_lable.replace("Rmean", "$R_{gap, mean}$")
    
    with open(PATH4TABLES+table_file, "w") as texfile:
        texfile.write(latex_lable)
    
print(code4insertion)
