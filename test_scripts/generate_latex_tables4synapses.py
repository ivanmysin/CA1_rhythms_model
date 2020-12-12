import pandas as pd

import sys
sys.path.append("../")
from basic_parameters import get_basic_params

PATH4TABLES = "/home/ivan/Документы/latex_supplement/"

def get_tabel_of_synapses(params, celltypes, synapse_params, celltype):
    table = pd.DataFrame(data=None, index=celltypes, columns=synapse_params)

    for conname, conndata in params["connections"].items():
        precell, postcell = conname.split("2")
        if postcell != celltype: continue

        # print(precell)
        for syn_param in synapse_params:
            table.loc[precell, syn_param] = conndata[syn_param]

    table.dropna(inplace=True)
    return table

def clear_latex_code(latex_lable):
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

    return latex_lable

def synapsic_tables(params):
    celltypes = sorted(list(set([neuron for neuron in params["CellParameters"].keys()])))
    synapse_params = [p for p in params["connections"]["ca3_spatial2pyr"].keys()]

    removed_syn_params = ["sourse_compartment", "NMDA", "Erev", "compartment2"]

    for rem in removed_syn_params:
        try:
            synapse_params.remove(rem)
        except ValueError:
            continue

    code4insertion = ""

    for celltype in celltypes:

        table = get_tabel_of_synapses(params, celltypes, synapse_params, celltype)

        if len(table) == 0:
            print(celltype)
            continue


        # print(table)
        table_file = celltype + "_synapses.tex"
        code4insertion += r"\input{" + table_file + "}\n"

        caption = "Synaptic connections to " + celltype
        caption = caption.replace("_", "\\_")

        label = celltype + "_synapses"
        latex_lable = table.to_latex(na_rep=" --- ", longtable=True, label=label, caption=caption)
        latex_lable = clear_latex_code(latex_lable)

        with open(PATH4TABLES+table_file, "w") as texfile:
            texfile.write(latex_lable)


    return code4insertion

def nmda_table(params):

    code4insertion = ""

    connames_with_nmda = []
    for key, val in params["connections"].items():
        if "NMDA" in val.keys():
            connames_with_nmda.append(key)
    connames_with_nmda = sorted(connames_with_nmda)

    synapse_params = [p for p in params["connections"]["ca3_spatial2pyr"]["NMDA"].keys()]

    removed_syn_params = ["sourse_compartment", "NMDA", "Erev", "compartment2"]

    for rem in removed_syn_params:
        try:
            synapse_params.remove(rem)
        except ValueError:
            continue

    synapse_params = ["Presynaptic", "Postsynaptic"] + synapse_params


    table = pd.DataFrame(data=None, index=connames_with_nmda, columns=synapse_params)
    for conname in connames_with_nmda:
        pre, post = conname.split("2")
        if pre.find("non_spatial") != -1: continue
        d = params["connections"][conname]["NMDA"]
        d["Presynaptic"] = pre
        d["Postsynaptic"] = post
        table.loc[conname] = pd.Series(d)

    table.dropna(inplace=True)
    print(table)
    table_file = "nmda_parameters.tex"
    code4insertion += r"\input{nmda_parameters}" + "\n"

    caption = "Parameters of NMDAR in the exite synapses"
    caption = caption.replace("_", "\\_")

    label = "nmda_parameters"
    latex_lable = table.to_latex(na_rep=" --- ", longtable=True, label=label, caption=caption, index=False)
    latex_lable = clear_latex_code(latex_lable)
    latex_lable = latex_lable.replace("_spatial", "")
    latex_lable = latex_lable.replace("gNMDAmax", "$g_{max, mean}, \ mS$")
    latex_lable = latex_lable.replace("tcon", "$\\tau_{rise}, \ ms$")
    latex_lable = latex_lable.replace("tcoff", "$\\tau_{decay}, \ ms$")
    latex_lable = latex_lable.replace("enmda", "$E_{NMDA}$, \ mV")

    with open(PATH4TABLES+table_file, "w") as texfile:
        texfile.write(latex_lable)

    return code4insertion

def gap_junctions_table(params):
    code4insertion = ""

    gapnames = sorted(params["gap_junctions_params"].keys())
    synapse_params = [p for p in params["gap_junctions_params"][gapnames[0]].keys()]

    removed_syn_params = ["sourse_compartment", "NMDA", "Erev", "compartment2"]

    for rem in removed_syn_params:
        try:
            synapse_params.remove(rem)
        except ValueError:
            continue
    synapse_params = ["Celltype", ] + synapse_params
    table = pd.DataFrame(data=None, index=synapse_params, columns=synapse_params)
    for conname in gapnames:
        pre, post = conname.split("2")
        if pre.find("non_spatial") != -1: continue
        d = params["gap_junctions_params"][conname]
        d["Celltype"] = pre

        table.loc[conname] = pd.Series(d)
    table = table.rename(columns={"r": "Rmean"})
    table.dropna(inplace=True)
    
    print(table)

    table_file = "gap_junctions_parameters.tex"
    code4insertion += r"\input{gap_junctions_parameters.tex}" + "\n"

    caption = "Parameters of gap junctions"
    caption = caption.replace("_", "\\_")

    label = "gap_junctions_parameters"
    latex_lable = table.to_latex(na_rep=" --- ", longtable=True, label=label, caption=caption, index=False)
    latex_lable = clear_latex_code(latex_lable)
    latex_lable = latex_lable.replace("_spatial", "")
    latex_lable = latex_lable.replace("gNMDAmax", "$g_{max, mean}, \ mS$")
    latex_lable = latex_lable.replace("tcon", "$\\tau_{rise}, \ ms$")
    latex_lable = latex_lable.replace("tcoff", "$\\tau_{decay}, \ ms$")
    latex_lable = latex_lable.replace("enmda", "$E_{NMDA}$, \ mV")

    with open(PATH4TABLES+table_file, "w") as texfile:
        texfile.write(latex_lable)

    return code4insertion

params = get_basic_params()

#code4insertion = synapsic_tables(params)
#code4insertion = nmda_table(params)
code4insertion = gap_junctions_table(params)
# synapse_params = [p for p in params["gap_junctions_params"]["pvbas2pvbas"].keys()]


print(code4insertion)
