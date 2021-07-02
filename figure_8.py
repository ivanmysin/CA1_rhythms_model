import numpy as np
import matplotlib.pyplot as plt
import h5py

from plot_result import plotting_param
from basic_parameters import get_basic_params

basic_params = get_basic_params()
filepath = basic_params["file_results"]


figfilepath = "./Results/figure_8.png"



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
fig, axes = plt.subplots(nrows=10, ncols=2, gridspec_kw=gridspec_kw, constrained_layout=True, figsize=(20, 20))

for ax in axes[:, 1]:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

rem_4ripple_ploting = ["ca3_non_spatial", "mec", "cckbas", "msteevracells", "msach", "aac"]


neuron_order = []
for celltype in plotting_param["neuron_order"]:
    if celltype in rem_4ripple_ploting:
        continue
    neuron_order.append(celltype)

tmin = 0
tmax = 400

with h5py.File(filepath, 'r') as h5file:
    t = h5file["time"][:]

    raw_lfp = h5file["extracellular/electrode_1/lfp/origin_data/channel_{}".format(plotting_param["number_pyr_layer"])][:]

    axes[0, 0].plot(t[:raw_lfp.size], raw_lfp, label="raw lfp")
    axes[0, 0].set_ylabel("mV")
    axes[0, 1].text(0, 0.5, "Raw LFP", fontsize="xx-large")



    slow_gamma_lfp = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/slow gamma".format(plotting_param["number_pyr_layer"])][:]

    ts = np.linspace(t[0], t[-1], slow_gamma_lfp.size)
    axes[1, 0].plot(ts, slow_gamma_lfp, label="slow gamma band")
    axes[1, 0].set_ylabel("mV")
    axes[1, 1].text(0, 0.5, "Slow gamma and \n ripple band of LFP", fontsize="xx-large")

    ripple_lfp = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/slow ripples".format(plotting_param["number_pyr_layer"])][:]
    axes[1, 0].plot(ts, ripple_lfp, label="ripples band")
    axes[1, 0].legend(loc='upper right')

    raster_group = h5file["extracellular/electrode_1/firing/origin_data"]

    axes[2, 0].set_title("Raster plots")
    for celltype_idx, celltype in enumerate(neuron_order):

        try:
            celltype_firings = raster_group[celltype]
        except KeyError:
            continue

        firings_x = np.empty(0, dtype=np.float)
        firings_y = np.empty(0, dtype=np.float)

        for cell_idx, cell_number in enumerate(sorted(celltype_firings.keys(), key=lambda x: int(x.split("_")[-1]))):
            firings_x = np.append(firings_x, celltype_firings[cell_number][:])
            firings_y = np.append(firings_y, np.zeros(celltype_firings[cell_number].size)+cell_idx)

        if firings_y.size == 0:
            firings_x = np.array([-1, -1])
            firings_y = np.array([0, 200])

        axes[celltype_idx+2, 0].scatter(firings_x, firings_y, s=3, color=plotting_param["neuron_colors"][celltype],  label=celltype)
        axes[celltype_idx+2, 1].text(0, 0.5, celltype, fontsize="xx-large")


for ax in axes[:, 0]:
    ax.set_xlim(tmin, tmax)

axes[-1, 0].set_xlabel("time, ms")


fig.savefig(figfilepath)
# plt.show()