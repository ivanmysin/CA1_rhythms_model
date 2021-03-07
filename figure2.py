import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt
from matplotlib import gridspec
import h5py
from basic_parameters import get_object_params
import processingLib as proclib
from plot_result import plotting_param


fig, axes = plt.subplots(nrows=28, ncols=1, sharex=True, figsize=(10, 30))

filepath = "/home/ivan/Data/CA1_simulation/theta_nice.hdf5"
figfilepath = "/home/ivan/Data/CA1_simulation/figure_2.png"

tmin = 0
tmax = 600

with h5py.File(filepath, 'r') as h5file:
    t = h5file["time"][:]

    raw_lfp = h5file["extracellular/electrode_1/lfp/origin_data/channel_{}".format(plotting_param["number_pyr_layer"])][:]

    axes[0].plot(t[:raw_lfp.size], raw_lfp, label="raw lfp")

    theta_lfp = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/theta".format(plotting_param["number_pyr_layer"])][:]
    axes[1].plot(t[:raw_lfp.size], theta_lfp, label="theta band")

    slow_gamma_lfp = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/slow gamma".format(plotting_param["number_pyr_layer"])][:]
    axes[2].plot(t[:raw_lfp.size], slow_gamma_lfp, label="slow gamma band")

    middle_gamma_lfp = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/middle gamma".format(plotting_param["number_pyr_layer"])][:]
    axes[3].plot(t[:raw_lfp.size], middle_gamma_lfp, label="middle gamma band")

    fast_gamma_lfp = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/fast gamma".format(plotting_param["number_pyr_layer"])][:]
    axes[4].plot(t[:raw_lfp.size], fast_gamma_lfp, label="fast gamma band")

    intracellular_group = h5file["intracellular/origin_data"]
    # intracell_keys = sorted(intracellular_group.keys(), key=lambda neur_num: int(neur_num.split("_")[-1]))
    raster_group = h5file["extracellular/electrode_1/firing/origin_data"]
    

    for celltype_idx, celltype in enumerate(plotting_param["neuron_order"]):
        for neuron_number in intracellular_group.keys():
            if celltype == intracellular_group[neuron_number].attrs["celltype"]:
                Vm = intracellular_group[neuron_number][:]
                axes[celltype_idx + 5].plot(t, Vm, label=celltype, color=plotting_param["neuron_colors"][celltype])
                break



        if celltype.find("ca3") != -1:
            celltype_ = "ca3"
        else:
            celltype_ = celltype

        celltype_firings = raster_group[celltype_]

        firings_x = np.empty(0, dtype=np.float)
        firings_y = np.empty(0, dtype=np.float)

        for cell_idx, cell_number in enumerate(sorted(celltype_firings.keys(), key=lambda x: int(x.split("_")[-1]))):
            firings_x = np.append(firings_x, celltype_firings[cell_number][:])
            firings_y = np.append(firings_y, np.zeros(celltype_firings[cell_number].size)+cell_idx)
            
        axes[celltype_idx+14].scatter(firings_x, firings_y, s=2, color=plotting_param["neuron_colors"][celltype],  label=celltype)

axes[0].set_xlim(tmin, tmax)

for ax in axes:
    ax.legend()
fig.savefig(figfilepath)
plt.show()