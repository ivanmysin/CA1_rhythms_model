import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import h5py
from basic_parameters import get_object_params
import processingLib as proclib
from plot_result import plotting_param
filepath = "/home/ivan/Data/CA1_simulation/theta_nice.hdf5"
figfilepath = "/home/ivan/Data/CA1_simulation/figure_3.png"



gridspec_kw = {
    "width_ratios" : [0.1, 0.5, 0.5, 0.5, 0.5, 1],
}
fig, axes = plt.subplots(nrows=14, ncols=6, gridspec_kw=gridspec_kw, constrained_layout=True, figsize=(10, 10))

for ax in axes[:, 0]:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')



with h5py.File(filepath, 'r') as h5file:


    
    distr_group = h5file["extracellular/electrode_1/firing/processing/phase_distrs"]

    for celltypes_idx, celltype in enumerate(plotting_param["neuron_order"]):
        for rhythm_idx, rhythm_name in enumerate(plotting_param["rhytms_order"]):

            if celltype.find("ca3") != -1:
                celltype_ = "ca3"
            else:
                celltype_ = celltype
            try:
                phase_distr = distr_group[celltype_][rhythm_name][:]
            except KeyError:
                continue

            rhythm_idx = rhythm_idx + 1
            phases = np.linspace(-np.pi, np.pi, phase_distr.size)
            signal4phase = np.max(phase_distr) * 0.25 * (np.cos(phases) + 1)
            axes[celltypes_idx, rhythm_idx].plot(phases, phase_distr, color=plotting_param["neuron_colors"][celltype])
            axes[celltypes_idx, rhythm_idx].plot(phases, signal4phase, color="black", linestyle="dotted")

            axes[celltypes_idx, rhythm_idx].set_xlim(-np.pi, np.pi)
            axes[celltypes_idx, rhythm_idx].set_ylim(0, None)

            if celltypes_idx == 0:
                axes[celltypes_idx, rhythm_idx].set_title(rhythm_name)

            if rhythm_idx == 0:
                axes[celltypes_idx, rhythm_idx].set_ylabel(celltype, rotation="horizontal", labelpad=20)

            if celltypes_idx == len(plotting_param["neuron_order"]) - 1:
                axes[celltypes_idx, rhythm_idx].set_xlabel("phase, rad")
            else:
                axes[celltypes_idx, rhythm_idx].tick_params(labelbottom=False, bottom=False)

            axes[celltypes_idx, 0].text(0, 0.5, celltype)

    gs = axes[-1, 0].get_gridspec()
    for ax in axes[0:5, -1]:
        ax.remove()
    axbig = fig.add_subplot(gs[0:5, -1])

    coup_group = h5file["extracellular/electrode_1/lfp/processing/theta_gamma_coupling/channel_" + str(
        plotting_param["number_pyr_layer"])]
    coupling = coup_group["coupling_matrix"][:]
    gamma_freqs = coup_group["gamma_freqs"][:]
    theta_phase = coup_group["theta_phase"][:]

    theta_signal = 5 * np.cos(theta_phase) + gamma_freqs[0] + 5

    axbig.plot(theta_phase, theta_signal, color="black", linestyle="dotted")

    # axbig.spines['right'].set_visible(False)
    # axbig.spines['top'].set_visible(False)
    # axbig.spines['left'].set_visible(False)
    # axbig.spines['bottom'].set_visible(False)
    # axbig.tick_params(labelbottom=False, bottom=False, labelleft=False, left=False)


    gr = axbig.pcolormesh(theta_phase, gamma_freqs, coupling, cmap="rainbow", shading='auto')
    axbig.set_xlim(-np.pi, np.pi)
    axbig.set_ylim(gamma_freqs[0], gamma_freqs[-1])
    axbig.set_ylabel("gamma frequency, Hz")
    axbig.set_xlabel("theta phase, rad")

    cbar = fig.colorbar(gr, ax=axbig)

    gs = axes[-1, 2].get_gridspec()
    for ax in axes[5:9, -1]:
        ax.remove()
    axbig2 = fig.add_subplot(gs[5:9, -1])

    gr_name = "extracellular/electrode_1/lfp/processing/theta_gamma_phase_phase_coupling/channel_"
    gr_name += str(plotting_param["number_pyr_layer"])
    coup_group = h5file[gr_name]
    nmarray = coup_group["nmarray"][:]
    for key, val in sorted(coup_group.items()):
        splited_key = key.split("_")
        if splited_key[0] != "coupling": continue

        diap = splited_key[-1] + " Hz"
        axbig2.plot(nmarray, val[:], label=diap)
    axbig2.set_ylim(0, 1.2)
    axbig2.legend(loc='upper right')
    axbig2.set_xlabel("n * theta phase")
    axbig2.set_ylabel("R of (n * theta phase - gamma phase) disrtibution")


    gs = axes[-1, 3].get_gridspec()
    for ax in axes[9:, -1]:
        ax.remove()
    axbig3 = fig.add_subplot(gs[9:, -1])

    mi_group = h5file["extracellular/electrode_1/lfp/processing/modulation_index/channel_" + str(plotting_param["number_pyr_layer"])]
    mi = mi_group["modulation_index"][:]
    freqs4ampl = mi_group["freqs4ampl"][:]
    freqs4phase = mi_group["freqs4phase"][:]

    gr = axbig3.pcolormesh(freqs4phase, freqs4ampl, mi, cmap="rainbow", shading='auto')
    axbig3.set_title("Modulation index")
    axbig3.set_xlim(4, None)
    axbig3.set_ylabel("frequencies for amplitude, Hz")
    axbig3.set_xlabel("frequencies for phase, Hz")
    cbar = fig.colorbar(gr, ax=axbig3)

fig.savefig(figfilepath)
# plt.show()