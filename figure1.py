import numpy as np
import sys
sys.path.append("./test_scripts")
import matplotlib.pyplot as plt
from nontheta_state_params import theta_state2non_theta_state_params
from basic_parameters_nice import get_object_params, get_basic_params

basic_params = get_basic_params()
pyr_idx = 0
# basic_params = theta_state2non_theta_state_params(basic_params)
pyr_coords = basic_params["pyr_coodinates"]
ca3_coords = basic_params["ca3_coodinates"]

print(pyr_coords[pyr_idx])



objects = get_object_params(Nthreads=1)

neurons = objects[0]["neurons"]
synapses = objects[0]["synapses_params"]



zero_pyr_idx = next(x for x, val in enumerate(objects[0]["cell_types_in_model"]) if val == "pyr")
zero_ca3_idx = next(x for x, val in enumerate(objects[0]["cell_types_in_model"]) if val == "ca3_spatial")

post_gid = pyr_idx + zero_pyr_idx

print(post_gid)
gmax_ca32pyr = []
gmax_coordca3 = []

# print(objects[0]["cell_types_in_model"])

for syn in synapses:
    # print(syn)
    if syn["post_gid"] != post_gid:
        continue

    if objects[0]["cell_types_in_model"][syn["pre_gid"]] != "ca3_spatial":
        continue

    pre_idx = syn["pre_gid"] - zero_ca3_idx
    # print(pre_idx)

    if pre_idx < 0:
        print("Below zero!!!!")

    gmax = syn["gmax"]

    gmax_ca32pyr.append(gmax)
    gmax_coordca3.append(pre_idx)

print(sum(gmax_ca32pyr))
plt.plot(gmax_coordca3, gmax_ca32pyr)
plt.show()

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