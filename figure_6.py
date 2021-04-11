import numpy as np
import matplotlib.pyplot as plt
import h5py

from plot_result import plotting_param
filepath = "/home/ivan/Data/CA1_simulation/theta_nice.hdf5" # "_ripples.hdf5"
figfilepath = "/home/ivan/Data/CA1_simulation/figure_6.png"
params = {'legend.fontsize': 'xx-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large'}
plt.rcParams.update(params)


gridspec_kw = {
    "width_ratios" : [1, 0.2],
}
fig, axes = plt.subplots(nrows=26, ncols=2, gridspec_kw=gridspec_kw, constrained_layout=True, figsize=(10, 30))

for ax in axes[:, 1]:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')




tmin = 0
tmax = 600

with h5py.File(filepath, 'r') as h5file:
    t = h5file["time"][:]

    raw_lfp = h5file["extracellular/electrode_1/lfp/origin_data/channel_{}".format(plotting_param["number_pyr_layer"])][:]

    axes[0, 0].plot(t[:raw_lfp.size], raw_lfp, label="raw lfp")
    axes[0, 0].set_ylabel("mV")
    axes[0, 1].text(0, 0.5, "Raw LFP")

    slow_gamma_lfp = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/slow gamma".format(plotting_param["number_pyr_layer"])][:]
    axes[1, 0].plot(t[:raw_lfp.size], slow_gamma_lfp, label="slow gamma band")
    axes[1, 0].set_ylabel("mV")
    axes[1, 1].text(0, 0.5, "Slow gamma band of LFP")

    ripple_lfp = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/slow ripples".format(plotting_param["number_pyr_layer"])][:]
    axes[2, 0].plot(t[:raw_lfp.size], ripple_lfp, label="ripples band")
    axes[2, 0].set_ylabel("mV")
    axes[2, 1].text(0, 0.5, "Ripples band of LFP")


    intracellular_group = h5file["intracellular/origin_data"]
    # intracell_keys = sorted(intracellular_group.keys(), key=lambda neur_num: int(neur_num.split("_")[-1]))
    raster_group = h5file["extracellular/electrode_1/firing/origin_data"]

    axes[3, 0].set_title("Intracellular potentials")
    for celltype_idx, celltype in enumerate(plotting_param["neuron_order"]):
        for neuron_number in intracellular_group.keys():
            if celltype == intracellular_group[neuron_number].attrs["celltype"]:
                Vm = intracellular_group[neuron_number][:]
                axes[celltype_idx + 3, 0].plot(t, Vm, label=celltype, color=plotting_param["neuron_colors"][celltype])

                axes[celltype_idx + 3, 1].text(0, 0.5, celltype)
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
            
        axes[celltype_idx+12, 0].scatter(firings_x, firings_y, s=2, color=plotting_param["neuron_colors"][celltype],  label=celltype)
        axes[celltype_idx+12, 1].text(0, 0.5, celltype)

    axes[12, 0].set_title("Raster of spikes")


for ax in axes[:, 0]:
    ax.set_xlim(tmin, tmax)

axes[-1, 0].set_xlabel("time, ms")


fig.savefig(figfilepath)
# plt.show()