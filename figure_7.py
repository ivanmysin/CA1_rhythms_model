import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt
params = {'legend.fontsize': 'xx-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'xx-large',
         'axes.titlesize':'xx-large',
         'xtick.labelsize':'xx-large',
         'ytick.labelsize':'xx-large'}
plt.rcParams.update(params)

import h5py
from plot_result import plotting_param
from basic_parameters import get_basic_params

basic_params = get_basic_params()
filepath = basic_params["file_results"]


figfilepath = "./Results/figure_7.png"

def plot_2pyr_connections(axes):

    from presimulation_lib import r2kappa
    x_pyr = 5000
    ca3_x = np.arange(0, 10000, 3)
    mec_x = np.arange(0, 10000, 3)
    pvbas_x = np.arange(0, 10000, 50)
    var_conns_on_pyr = 9000

    # print(ca3_x)

    ca32pyr = np.exp(-0.5 * (x_pyr - ca3_x) ** 2 / var_conns_on_pyr) / (np.sqrt(var_conns_on_pyr * 2 * np.pi))
    pvbas2pyr = np.exp(-0.5 * ((x_pyr - pvbas_x + 0.000001) ** -2) / var_conns_on_pyr) / (
        np.sqrt(var_conns_on_pyr * 2 * np.pi))

    kappa, i0 = r2kappa(0.9)
    mec2pyr = np.exp(kappa * np.cos(2 * np.pi * 0.1 * 0.001 * (x_pyr - mec_x - 500)))

    mec2pyr = 0.5 * mec2pyr / np.max(mec2pyr)
    ca32pyr = ca32pyr / np.max(ca32pyr)
    pvbas2pyr = 0.1 * pvbas2pyr / np.max(pvbas2pyr)

    axes.plot(0.001*ca3_x, ca32pyr, color=plotting_param["neuron_colors"]["ca3_spatial"], label="ca3")
    axes.plot(0.001*mec_x, mec2pyr, color=plotting_param["neuron_colors"]["mec"], label="mec")
    axes.plot(0.001*pvbas_x, pvbas2pyr, color=plotting_param["neuron_colors"]["pvbas"], label="pvbas")
    axes.set_xlim(0, 10)
    axes.set_ylim(0, 1.2)
    axes.set_ylabel("Weight")
    axes.set_xlabel("time coordinates, sec")
    axes.legend()



firing4plot = ["pyr", "pvbas", "ca3_spatial", "mec"]
simtime = 10000
npyr4preces = 3
intracell_pyr_neuron = "neuron_12110"


gridspec_kw = {
    "width_ratios" : [0.01, 0.5, 0.5, 0.5, 0.5, 1],
}

pyr_dx = 3
Npyr = 9000
fig = plt.figure(constrained_layout=True, figsize=(15, 15))
pyr_coords = np.cumsum( np.zeros(Npyr) + pyr_dx )
pyr_coords[pyr_coords.size//2:] = np.nan

place_centers = []
indicesofpyr = []
pyrfirsize = []

with h5py.File(filepath, 'r') as h5file:
    raster_group = h5file["extracellular/electrode_1/firing/origin_data"]
    intracellular_group = h5file["intracellular/origin_data"]
    theta_signal = h5file["extracellular/electrode_1/lfp/processing/bands/channel_{}/theta".format(plotting_param["number_pyr_layer"])][:]
    theta_phases = np.angle(hilbert(theta_signal))
    # theta_phases[theta_phases < 0] += 2 * np.pi
    sampling_rate = h5file["extracellular/electrode_1/lfp/origin_data"].attrs["SamplingRate"]


    gs1 = fig.add_gridspec(nrows=5, ncols=npyr4preces+1)  # , left=0.05, right=0.48, wspace=0.05

    for fir_idx, celltype in enumerate(firing4plot):

        celltype_firings = raster_group[celltype]

        firings_x = np.empty(0, dtype=np.float)
        firings_y = np.empty(0, dtype=np.float)

        for cell_idx, cell_number in enumerate(sorted(celltype_firings.keys(), key=lambda x: int(x.split("_")[-1]))):
            firings_x = np.append(firings_x, celltype_firings[cell_number][:])
            firings_y = np.append(firings_y, np.zeros(celltype_firings[cell_number].size) + cell_idx)

            if celltype == "pyr" and cell_idx < 3500: # and cell_idx > 100
                pyrfirsize.append(celltype_firings[cell_number].size)
                indicesofpyr.append(cell_number)
                place_centers.append(pyr_coords[cell_idx])

                if cell_number == intracell_pyr_neuron:
                    intracell_center = pyr_coords[cell_idx]

        ax0 = fig.add_subplot(gs1[fir_idx, 0])
        ax0.set_xlim(0, 1)
        ax0.set_ylim(0, 1)
        ax0.axis('off')

        ax1 = fig.add_subplot(gs1[fir_idx, 1:])
        ax1.scatter(0.001*firings_x, firings_y, s=0.2, color=plotting_param["neuron_colors"][celltype])
        ax1.set_xlim(0, 0.001*simtime)
        ax1.set_ylim(0, cell_idx+1)

        ax0.text(0.5, 0.5, celltype, fontsize="xx-large")

        if fir_idx == 0:
            ax1.set_title("Raster of spikes")
            ax1.text(-1, 10000, "A", fontsize=20, weight="bold")

        if fir_idx == len(firing4plot)-1:
            ax1.set_xlabel("time, sec")

    pyrfirsort = np.argsort(-1*np.asarray(pyrfirsize) )

    ax1 = fig.add_subplot(gs1[len(firing4plot), 1])
    for pyr_idx in range(3500): # npyr4preces
        # ax1 = fig.add_subplot(gs1[len(firing4plot), pyr_idx + 1])

        fir = 0.001 * raster_group["pyr"][ indicesofpyr[ pyrfirsort[pyr_idx] ] ][:]



        place_center = place_centers[ pyrfirsort[pyr_idx] ] * 0.001 # np.median(fir)
        if np.isnan(place_center):
            continue

        fir_during_place = fir - place_center - 0.2


        is_inside = np.abs(fir_during_place) < 2.0


        if np.sum(is_inside) < 12: continue


        fir_phases = theta_phases[np.floor(fir*sampling_rate).astype(np.int) - 1]



        ax1.scatter(fir_during_place, fir_phases, s=2, color=plotting_param["neuron_colors"]["pyr"])

    ax1.set_xlim(-1.5, 1.5)
    # ax1.set_xticklabels(ax1.get_xticks(), rotation = -45)
    ax1.set_ylim(-np.pi, np.pi)
    ax1.set_ylabel("theta phase, rad")
    ax1.set_xlabel("time, sec")

    ax1.text(-2, 3.14, "B", fontsize=20, weight="bold")

    ax2 = fig.add_subplot(gs1[len(firing4plot), 2:])

    plot_2pyr_connections(ax2)

    ax2.text(-1, 1.2, "C", fontsize=20, weight="bold")



fig.savefig(figfilepath)
# plt.show()