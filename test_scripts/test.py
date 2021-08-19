import numpy as np
import os
import h5py
from elephant import signal_processing as sigp
import matplotlib.pyplot as plt
from scipy.signal.windows import parzen
filepath = "/home/ivan/Data/CA1_simulation/LFP_by_threads/theta_state.hdf5"  # "/home/ivan/PycharmProjects/CA1_rhythms_model/Results/theta_state.hdf5"
files_path = "/home/ivan/Data/CA1_simulation/LFP_by_threads/"

import pickle

filehandler = open("../Results/params", 'rb')
objc_p = pickle.load(filehandler)

counter = 1
for cell in objc_p[1]["neurons"]:
    if cell["celltype"] != "pyr": continue

    print(cell["gid"])
    counter += 1
# print(counter)
#
#
# counter = 1
# for cell in objc_p[55]["neurons"]:
#     if cell["celltype"] != "pyr": continue
#     # print(cell["celltype"])
#     counter += 1
print(counter)


filehandler.close()
# fig, axes = plt.subplots(nrows=2)
#
# with h5py.File(filepath, 'r') as h5file:
#      lfp = h5file["extracellular/electrode_1/lfp/origin_data/channel_9"][:]
#
# t = np.linspace(0, 10.2, lfp.size)
#
# axes[0].plot(t, lfp)
#
# lfp_sum = 0
#
# for file in os.listdir(files_path):
#     if not file[0].isdigit(): continue
#
#     with h5py.File(files_path + file, 'r') as h5file:
#         lfp = h5file["9"][:]
#
#
#     if np.max(lfp) > 8:
#         print(file)
#         continue
#
#     lfp_sum += lfp
#
#
# axes[1].plot(t, lfp_sum)




# n_pyr = 10
# start = 1000
#
# Npyr = 9000
# pyr_dx = 3
# pyr_coord = np.cumsum( np.zeros(Npyr) + pyr_dx )
# # print(pyr_coord[200], pyr_coord[300])
# # print(pyr_coord[400], pyr_coord[1400])
#
# def get_spikerate(celltype_group, celltype, size):
#     spike_rate = np.zeros(size, dtype=np.float)
#     for sp_idx, (cell_key, firing) in enumerate(sorted(celltype_group.items(), key=lambda x: int(x[0].split("_")[-1]),)):
#          if celltype == "pyr" and (sp_idx < 400 or sp_idx > 1400): continue
#
#          spike_rate[ (np.floor( 0.001 * firing[:] * fd ) ).astype(np.int) ] += 1
#
#     spike_rate = np.convolve(spike_rate, parzen(951), mode="same")
#     return spike_rate
#
# with h5py.File(filepath, 'r') as h5file:
#     t = h5file["time"][:]
#     fd = 1000 / (t[1] - t[0])
#
#     lfp = h5file["extracellular/electrode_1/lfp/origin_data/channel_1"][:]
#
#     intracellular_group = h5file["intracellular/origin_data"]
#
#     fig, axes = plt.subplots(nrows=11, sharex=True, figsize=(15, 10))
#     axes[0].plot(t[:lfp.size], lfp, color="black")
#
#     start_idx = 1
#     Vpyr = 0
#     for celltype_name, cell_V in intracellular_group.items():
#         if intracellular_group[celltype_name].attrs["celltype"] != "pyr": continue
#
#
#         axes[start_idx].plot(t, cell_V[:], color="blue")
#
#         axes[start_idx].hlines(-10, t[0], t[-1], color="red")
#         #Vpyr += cell_V[:]
#
#         if start_idx == 9 :
#             break
#         start_idx += 1



    #Vpyr = Vpyr / start_idx



plt.show()






########################################################################################


"""
fig, axes = plt.subplots(nrows=2, sharex=True, figsize=(15, 10))
axes[0].plot(t[:lfp.size], lfp, color="black")

# print(t.size)
celltype = "pyr"
celltype_group = h5file["extracellular/electrode_1/firing/origin_data/" + celltype]
pyr_spike_rate = get_spikerate(celltype_group, celltype, t.size)

celltype = "pvbas"
celltype_group = h5file["extracellular/electrode_1/firing/origin_data/" + celltype]
pvbas_spike_rate = get_spikerate(celltype_group, celltype, t.size)

axes[1].plot(t, pyr_spike_rate, color="red")
axes[1].plot(t, pvbas_spike_rate, color="green")
"""







# N = 9000
# radius_for_pyramids = 50
# pyr_coord_in_layer_x = radius_for_pyramids * 2 * (np.random.rand(N) - 0.5)
# pyr_coord_in_layer_y = radius_for_pyramids * 2 * (np.random.rand(N) - 0.5)
#
# is_big_dist = np.sqrt(pyr_coord_in_layer_x**2 + pyr_coord_in_layer_y**2) <= radius_for_pyramids
#
# pyr_coord_in_layer_x = pyr_coord_in_layer_x[is_big_dist]
# pyr_coord_in_layer_y = pyr_coord_in_layer_y[is_big_dist]
#
# plt.scatter(pyr_coord_in_layer_x, pyr_coord_in_layer_y, s=0.5)
# plt.show()