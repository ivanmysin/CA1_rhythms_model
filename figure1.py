
import numpy as np
import matplotlib.pyplot as plt
from presimulation_lib import r2kappa
x_pyr = 5000
ca3_x = np.arange(0, 10000, 3)
mec_x = np.arange(0, 10000, 3) # = np.linspace(-np.pi, np.pi, 3500)
pvbas_x = np.arange(0, 10000, 50)
var_conns_on_pyr = 9000


# print(ca3_x)

ca32pyr = np.exp(-0.5*(x_pyr - ca3_x)**2 / var_conns_on_pyr) / (np.sqrt(var_conns_on_pyr * 2 * np.pi ))
pvbas2pyr = np.exp(-0.5* ((x_pyr - pvbas_x + 0.000001)**-2) / var_conns_on_pyr) / (np.sqrt(var_conns_on_pyr * 2 * np.pi ))


kappa , i0 = r2kappa(0.9)
mec2pyr = np.exp(kappa * np.cos(2*np.pi*0.1*0.001*(x_pyr-mec_x-500) )  )



mec2pyr = 0.5 * mec2pyr  / np.max(mec2pyr)
ca32pyr = ca32pyr  / np.max(ca32pyr)
pvbas2pyr = 0.1 * pvbas2pyr  / np.max(pvbas2pyr)

fig, axes = plt.subplots(nrows=2, ncols=1)

axes[0].plot(ca3_x, ca32pyr, color="orange", label="ca3")
axes[0].plot(mec_x, mec2pyr, color="red", label="mec")
axes[0].plot(pvbas_x, pvbas2pyr, color="blue", label="pvbas")
axes[0].set_xlim(0, 10000)
axes[0].set_ylim(0, 1)
axes[0].set_ylabel("Relative weight of connections")
axes[0].set_xlabel("Time of pyramidal neuron, ms")
axes[0].legend()
plt.show()



"""



import numpy as np
import presimulation_lib as prelib
import sys
sys.path.append("./test_scripts")
import matplotlib.pyplot as plt
from nontheta_state_params import theta_state2non_theta_state_params
from basic_parameters_nice import get_object_params, get_basic_params

basic_params = get_basic_params()
pyr_idx = 0
# basic_params = theta_state2non_theta_state_params(basic_params)
# pyr_coords = basic_params["pyr_coodinates"]
# ca3_coords = basic_params["ca3_coodinates"]


pvbas_coords = basic_params["pvbas_coodinates"]

# print(ca3_coords.max())
# print(pyr_coords[pyr_idx])

pre_name = "ca3_spatial"


objects = get_object_params(Nthreads=1)

neurons = objects[0]["neurons"]

# for n in neurons:
#     if n["celltype"] == "mec":
#         print(n["cellparams"]["grid_phase"])


synapses = objects[0]["synapses_params"]

print("Number of synapses ", len(synapses))

zero_pyr_idx = next(x for x, val in enumerate(objects[0]["cell_types_in_model"]) if val == "pyr")
zero_pre_idx = next(x for x, val in enumerate(objects[0]["cell_types_in_model"]) if val == pre_name)

zero_pvbas_idx = next(x for x, val in enumerate(objects[0]["cell_types_in_model"]) if val == "pvbas")

post_gid = pyr_idx + zero_pyr_idx

print(zero_pre_idx)


gmax_pre2pyr = []
gmax_ca32pyr = []
pre_coords = []
ca3_coords = []

pvbas_coord = []
gmax_pvbas2pyr = []

# print(objects[0]["cell_types_in_model"])

for syn in synapses:


    if syn["post_gid"] != post_gid:
        continue

    # if objects[0]["cell_types_in_model"][syn["pre_gid"]] != pre_name:
    #     continue



    # pre_idx = syn["pre_gid"] - zero_pre_idx
    # # print(pre_idx)
    #
    # if pre_idx < 0:
    #     print("Below zero!!!!")

    gmax = syn["gmax"]

    cell = neurons[syn["pre_gid"]]

    if cell["celltype"] == "mec":

        grid_phase = cell["cellparams"]["grid_phase"]
        # pre_coords.append(ca3_coords[pre_idx])

        grid_centers = 1000 * prelib.get_grid_centers(0.1, grid_phase, 10)
        if grid_centers.size == 0:
            continue
        pre_coords.append( grid_centers[np.argmin( (grid_centers-5000)**2)] )
        gmax_pre2pyr.append(gmax)

    elif cell["celltype"] == "ca3_spatial":
        gmax_ca32pyr.append(gmax)
        ca3_coords.append(cell["cellparams"]["place_center_t"])

    elif cell["celltype"] == "pvbas":

        cell_idx = cell["gid"] - zero_pvbas_idx
        print(cell_idx)
        pvbas_coord.append(pvbas_coords[ cell_idx ])  #
        gmax_pvbas2pyr.append(gmax)





print(sum(gmax_pre2pyr))
# plt.scatter(pre_coords, gmax_pre2pyr)
# plt.scatter(ca3_coords, gmax_ca32pyr)
plt.scatter(pvbas_coord, gmax_pvbas2pyr)
plt.show()
"""




"""
import numpy as np
import matplotlib.pyplot as plt


tpyr = 5000
tpvbas = 5000
ca3_coord_x = np.cumsum( np.zeros(3500) + 3)
pvbas_coord_x = np.cumsum( np.zeros(200) + 50)
var_conns_on_pyr = 1000
var_conns_on_pvbas = var_conns_on_pyr * 3
# mec_coord_x

ca32pyr = np.exp(-0.5*(ca3_coord_x - tpyr)**2/var_conns_on_pyr) / (2*np.pi*var_conns_on_pyr)
ca32pvbas = np.exp(-0.5*(ca3_coord_x - tpvbas)**2/var_conns_on_pvbas) / (2*np.pi*var_conns_on_pvbas)
pvbas2pyr = np.exp(-0.5*( (pvbas_coord_x - tpyr)+0.00001 )**-2/var_conns_on_pyr) / (2*np.pi*var_conns_on_pyr)

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 5))

axes[0].plot(ca3_coord_x, ca32pyr, label="ca3")
axes[0].plot(pvbas_coord_x, pvbas2pyr, label="pvbas")

axes[1].plot(ca3_coord_x, ca32pvbas, label="ca3")
plt.show()
"""