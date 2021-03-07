import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from elephant import signal_processing as sigp
import h5py

filepath =  "/home/ivan/Data/CA1_simulation/test_fast_gamma_at_theta_state.hdf5"

with h5py.File(filepath, 'r') as h5file:
    t = h5file["time"][:]
    dt = t[1] - t[0]
    fd = 1000 / dt
    el_z = np.linspace(-200, 600, 10)
    raster_group = h5file["extracellular/electrode_1/firing/origin_data"]
    # common_coup_group = h5file["extracellular/electrode_1/lfp/processing/theta_gamma_coupling"]

    # for coup_group_key, coup_group in sorted( common_coup_group.items(), key=lambda x: int(x[0].split("_")[-1]) ):
    #
    #     coupling = coup_group["coupling_matrix"][:]
    #     gamma_freqs = coup_group["gamma_freqs"][:]
    #     theta_phase = coup_group["theta_phase"][:]
    #
    #     theta_signal = np.cos(theta_phase)
    #
    #     fig = plt.figure(figsize=(5, 5))
    #     fig.suptitle(coup_group_key)
    #     gs = gridspec.GridSpec(2, 2, figure=fig, height_ratios=[1, 10], width_ratios=[10, 1], hspace=0)
    #
    #     axes = plt.subplot(gs[0, 0])
    #     axes.plot(theta_phase, theta_signal, color="black")
    #     axes.set_xlim(-np.pi, np.pi)
    #     axes.spines['right'].set_visible(False)
    #     axes.spines['top'].set_visible(False)
    #     axes.spines['left'].set_visible(False)
    #     axes.spines['bottom'].set_visible(False)
    #     axes.tick_params(labelbottom=False, bottom=False, labelleft=False, left=False)
    #
    #     axes = plt.subplot(gs[1, 0])
    #     gr = axes.pcolormesh(theta_phase, gamma_freqs, coupling, cmap="rainbow", shading='auto')
    #     axes.set_xlim(-np.pi, np.pi)
    #     axes.set_ylabel("gamma frequency, Hz")
    #     axes.set_xlabel("theta phase, rad")
    #
    #     axes = plt.subplot(gs[1, 1])
    #     cbar = fig.colorbar(gr, cax=axes)
    #
    #     plt.show()


    lfp_group = h5file["extracellular/electrode_1/lfp/origin_data"]
    # wavelet_group = h5file["extracellular/electrode_1/lfp/processing/wavelet"]

    bands_group = h5file["extracellular/electrode_1/lfp/processing/bands"]
    #
    theta = bands_group["channel_4/theta"][:]
    fast_gamma = bands_group["channel_4/fast gamma"][:]
    #
    # fig, axes = plt.subplots(nrows=2, sharex=True)
    # axes[0].plot(t[:fast_gamma.size], fast_gamma)
    # axes[0].plot(t[:fast_gamma.size], theta)
    #
    # uniq_celltypes = raster_group.keys()
    #
    # for celltype in uniq_celltypes:
    #     if celltype != "pyr": continue
    #
    #     sp_idx = 0
    #     for cell_key, firing in raster_group[celltype].items():
    #         # celltype_idx = int(cell_key.split("_")[-1])
    #
    #         axes[1].scatter(firing, np.zeros(firing.size) + sp_idx + 1, color="b", s=1)
    #
    #         sp_idx += 1
    #
    #     axes[1].set_ylim(1, sp_idx)
    #
    #
    #
    # plt.show()


    # ampls = []
    # middle_ampls = []
    # slow_ampls = []
    # theta_ampls = []
    # for bandkey, bands in sorted( bands_group.items(), key=lambda x: int(x[0].split("_")[-1]) ):

        # theta = bands["theta"][:]
        # ta = np.std(theta)
        # theta_ampls.append(ta)


        # fast_gamma = bands["fast gamma"][:]
        # middle_gamma = bands["middle gamma"][:]
        # slow_gamma = bands["slow gamma"][:]

        # famp = np.std(fast_gamma)
        # ampls.append(famp)
        # middle_ampls.append( np.std(middle_gamma) )
        # slow_ampls.append( np.std(slow_gamma)  )

        # plt.plot(t[:theta.size], theta)
        # plt.plot(t[:theta.size], fast_gamma)
        # plt.show()
    intracellular_group = h5file["intracellular/origin_data"]
    intracell_keys = intracellular_group.keys()

    fig, axes = plt.subplots(nrows=3, sharex=True, figsize=(5, 10))
    axes[0].plot(t[:theta.size], theta, color="black")
    axes[2].plot(t[:theta.size], fast_gamma, color="blue")


    for celltype_idx, celltype in enumerate(["pyr"]):
        for key in intracell_keys:
            if intracellular_group[key].attrs["celltype"] != celltype: continue

            celltype_idx += 1
            v = intracellular_group[key][:]

            sigp.butter(v, highpass_freq=90, lowpass_freq=150, order=2, fs=fd)


            celltype = intracellular_group[key].attrs["celltype"]
            axes[celltype_idx].plot(t, v, label=celltype, color="red")
            axes[celltype_idx].legend()

            axes[celltype_idx].set_xlim(t[0], t[-1])
            axes[celltype_idx].set_ylim(-90, 60)

            # if celltype_idx == len(plotting_param["neuron_order"]):
            #     axes[celltype_idx].set_xlabel("time, ms")
            #     axes[celltype_idx].tick_params(labelbottom=True, bottom=True)
            # else:
            #     axes[celltype_idx].tick_params(labelbottom=False, bottom=True)
            # axes[celltype_idx].set_ylabel("mV")

    plt.show()

# plt.plot(el_z, ampls, label="Fast gamma")
# plt.plot(el_z, middle_ampls, label="Middle gamma")
# plt.plot(el_z, slow_ampls, label="Slow gamma")
# plt.plot(el_z, slow_ampls, label="Slow gamma")
# plt.plot(el_z, theta_ampls, label="Theta")
# plt.legend()
# plt.show()
