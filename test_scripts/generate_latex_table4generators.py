import pandas as pd

import sys
sys.path.append("../")
from basic_parameters import get_basic_params

PATH4TABLES = "/home/ivan/Документы/latex_supplement/"

def get_tables_of_parameters(params, gentype):
    genparam = params["CellParameters"]

    artgens = []
    for genkey, genval in genparam.items():
        if genval["cellclass"] == gentype:
            artgens.append(genkey)

    params_names = sorted( genparam[artgens[0]].keys() )
    rem_arr = ["cellclass", "delta_t", "grid_phase", "place_center_t"]
    for rem in rem_arr:
        try:
            params_names.remove(rem)
        except ValueError:
            continue


    table = pd.DataFrame(data=None, index=params_names, columns=artgens)

    for genkey in sorted(artgens):
        for param in params_names:
            val = genparam[genkey][param]
            table.loc[param, genkey] = val

    print(table)
    table_file = gentype + "_parameters.tex"
    code4insertion = r"\input{" + table_file + "}" + "\n"
    caption = "Parameters of artifitial generators"
    label = gentype + "_parameters"
    latex_lable = table.to_latex(na_rep=" --- ", longtable=True, label=label, caption=caption, index=True)

    if gentype == "ArtifitialCell":
        latex_lable = latex_lable.replace("R", "$R_{\\theta}$")
        latex_lable = latex_lable.replace("freqs", "$\omega_{\\theta},\\ Hz$")
        latex_lable = latex_lable.replace("mu  ", r"$\mu_{\theta},\ rad$")

    elif  gentype == "ArtifitialGridCell" or gentype == "ArtifitialPlaceCell":
        latex_lable = latex_lable.replace("Rtheta", "$R_{\\theta}$")
        latex_lable = latex_lable.replace("Rgamma", "$R_{\\gamma}$")
        latex_lable = latex_lable.replace("Rgrid", "$R_{grid}$")
        latex_lable = latex_lable.replace("low\\_freqs", "$\\omega_{\\theta},\\ Hz$")
        latex_lable = latex_lable.replace("high\\_freqs", "$\\omega_{\\gamma},\\ Hz$")
        latex_lable = latex_lable.replace("grid\\_freqs", "$\\omega_{grid},\\ Hz$")
        latex_lable = latex_lable.replace("high\\_mu", "$\\mu_{\\gamma},\ rad$")
        latex_lable = latex_lable.replace("low\\_mu", "$\\mu_{\\theta},\ rad$")
        latex_lable = latex_lable.replace("place\\_t\\_radius", "$r_{place}, \\ ms$")

    latex_lable = latex_lable.replace("spike\\_rate", r"$S$")
    latex_lable = latex_lable.replace("latency", r"$latency,\ ms$")
    latex_lable = latex_lable.replace("3.14159", r"$\pi$")

    with open(PATH4TABLES + table_file, "w") as texfile:
        texfile.write(latex_lable)

    return code4insertion

params = get_basic_params()
# gentype = "ArtifitialCell"
# code4insertion = get_tables_of_parameters(params, gentype)
# gentype = "ArtifitialGridCell"
# code4insertion = get_tables_of_parameters(params, gentype)

gentype = "ArtifitialPlaceCell"
code4insertion = get_tables_of_parameters(params, gentype)
print(code4insertion)