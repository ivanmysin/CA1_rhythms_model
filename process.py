import numpy as np
from elephant import signal_processing as sigp 
import matplotlib.pyplot as plt
import h5py
import processingLib as plib
from scipy.stats import zscore
from scipy.ndimage import zoom

processing_param = {


    "morlet_w0" : 12.0,      # центральная частота для вейвлета Морле
    "freqs_step" : 10,      # количество частот, для которых вычисляется вейвлет за один цикл 
    "max_freq_lfp" : 500,   # Гц, анализируем только до этой частоты 

    "number_pyr_layer" : 1, # number of channel from pyramidal layer

    "butter_order" : 2,     # Порядок для фильтра Баттерворда
    "filt_bands" : {
        "delta" : [1, 4], 
        "theta" : [4, 12], 
        "slow gamma" : [25, 50], 
        "fast gamma" : [50, 120], 
        # "slow ripples" : [80, 250], 
        # "fast ripples" : [200, 500], 
   
    },

    "freqs4theta_gamma_coupling" : [30, 150],

    "gamma_bands4phase_phase_coupling": [ [30, 90], [30, 40], [40, 60], [50, 70], [60, 80], ],
    "nmarray" : np.arange(1, 14),

    "modulation_index": {
        "freqs4phase" : [2, 20],
        "freqs4amplitude" : [20, 150],
    },

    "upsamling4csd" : 20,

}



def processing_and_save(filepath):
    with h5py.File(filepath, 'a') as h5file:
        # t = h5file["time"][:]

        lfp_group = h5file["extracellular/electrode_1/lfp"]
        lfp_group_origin = lfp_group["origin_data"]

        try:
            process_group = lfp_group.create_group("processing")
        except ValueError:
            del h5file["extracellular/electrode_1/lfp/processing"]
            process_group = lfp_group.create_group("processing")

        wavelet_group = process_group.create_group("wavelet")
        bands_group = process_group.create_group("bands")

        theta_gamma_coupling_group = process_group.create_group("theta_gamma_coupling")
        theta_gamma_phase_phase_coupling_group = process_group.create_group("theta_gamma_phase_phase_coupling")
        modulation_index_group = process_group.create_group("modulation_index")

        fd = lfp_group_origin.attrs["SamplingRate"]

        lfp_keys = lfp_group_origin.keys()

        for key_idx in range(len(lfp_keys)):
            key = "channel_" + str(key_idx + 1)
            lfp = lfp_group_origin[key][:]

            freqs = np.fft.rfftfreq(lfp.size, d=1/fd)
            freqs = freqs[1:]  # remove 0 frequency
            freqs = freqs[freqs <= processing_param["max_freq_lfp"] ]  # remove frequencies below 500 Hz


            channel_wavelet_group = wavelet_group.create_group(key)

            channel_wavelet_group.create_dataset("frequecies", data=freqs)
            wdset = channel_wavelet_group.create_dataset("wavelet_coeff", (len(freqs), len(lfp)), dtype="c16")

            for start_idx in range(0, freqs.size, processing_param["freqs_step"]):
                end_idx = start_idx + processing_param["freqs_step"]

                if end_idx > freqs.size:
                    end_idx = freqs.size

                W = sigp.wavelet_transform(lfp, freqs[start_idx:end_idx], nco=processing_param["morlet_w0"], fs=fd)
                wdset[start_idx:end_idx, : ] = W


            #####################################
            channel_bands_group = bands_group.create_group(key)
            # lfp = zscore(lfp)
            for band_name, freq_lims in processing_param["filt_bands"].items():
                filtered_signal = sigp.butter(lfp, highpass_freq=freq_lims[0], \
                    lowpass_freq=freq_lims[1], order=processing_param["butter_order"], fs=fd )

                channel_bands_group.create_dataset(band_name, data = filtered_signal)
            #####################################
            # theta-gamma phase amplitude coupling

            channel_theta_gamma_coupling_group = theta_gamma_coupling_group.create_group(key)
            phase_signal = channel_bands_group["theta"][:]
            gamma_freqs = channel_wavelet_group["frequecies"][:]


            is_gamma_freqs = (gamma_freqs>=processing_param["freqs4theta_gamma_coupling"][0])&(gamma_freqs<=processing_param["freqs4theta_gamma_coupling"][1])
            coefAmp = channel_wavelet_group["wavelet_coeff"][:]
            coefAmp = coefAmp[is_gamma_freqs, :]
            gamma_freqs = gamma_freqs[is_gamma_freqs]
            phasebins = 50
            coupling = plib.cossfrequency_phase_amp_coupling(phase_signal, coefAmp, phasebins=phasebins, nkernel=15)

            channel_theta_gamma_coupling_group.create_dataset("coupling_matrix", data = coupling)
            channel_theta_gamma_coupling_group.create_dataset("gamma_freqs", data = gamma_freqs)
            channel_theta_gamma_coupling_group.create_dataset("theta_phase", data = np.linspace(-np.pi, np.pi, phasebins))

            ####################################################################################
            # theta-gamma phase phase coupling
            channel_theta_gamma_phase_phase_coupling_group = theta_gamma_phase_phase_coupling_group.create_group(key)

            phase_signal = channel_bands_group["theta"][:]
            couplings, binss, distrss = plib.phase_phase_coupling(phase_signal, lfp, processing_param["gamma_bands4phase_phase_coupling"], \
                    fd, processing_param["nmarray"], thresh_std=None, circ_distr=True, butter_order=processing_param["butter_order"])

            channel_theta_gamma_phase_phase_coupling_group.create_dataset("nmarray" , data = processing_param["nmarray"])
            channel_theta_gamma_phase_phase_coupling_group.create_dataset("bins", data=binss)
            for band_idx, phase_phase_band in enumerate(processing_param["gamma_bands4phase_phase_coupling"]):
                diap_name = "_" + str(phase_phase_band[0]) + "-" + str(phase_phase_band[1])
                channel_theta_gamma_phase_phase_coupling_group.create_dataset("coupling"+diap_name , data = couplings[band_idx])
                channel_theta_gamma_phase_phase_coupling_group.create_dataset("distrs"+diap_name , data = distrss[band_idx])

            ####################################################################################
            # phase amplidute modulation index
            channel_modulation_index_group = modulation_index_group.create_group(key)
            
            freqs = channel_wavelet_group["frequecies"][:] 
            freqs4phase_sl = plib.slice_by_bound_values(freqs, processing_param["modulation_index"]["freqs4phase"][0], processing_param["modulation_index"]["freqs4phase"][1])
            freqs4ampl_sl = plib.slice_by_bound_values(freqs, processing_param["modulation_index"]["freqs4amplitude"][0], processing_param["modulation_index"]["freqs4amplitude"][1])
                        
            
            W4phase = channel_wavelet_group["wavelet_coeff"][freqs4phase_sl, :]
            W4ampls = channel_wavelet_group["wavelet_coeff"][freqs4ampl_sl, :]
            
            mi = plib.get_modulation_index(W4phase, W4ampls, nbins=20)
            
            channel_modulation_index_group.create_dataset("freqs4phase", data=freqs[freqs4phase_sl])
            channel_modulation_index_group.create_dataset("freqs4ampl", data=freqs[freqs4ampl_sl])
            channel_modulation_index_group.create_dataset("modulation_index", data=mi)





        ####################################################################################
        # current source density
        current_source_density_group = process_group.create_group("current_source_density")

        for band_name in processing_param["filt_bands"].keys():
            lfp_band_list = []
            for channel_name, channel_group in sorted(process_group["bands"].items(), key=lambda x: int(x[0].split("_")[-1]) ):
                lfp_band_list.append(channel_group[band_name][:])

            csd = plib.current_sourse_density(lfp_band_list, dz=1)
            csd = zoom(csd, zoom=(processing_param["upsamling4csd"], 1), mode="nearest")
            current_source_density_group.create_dataset(band_name, data=csd)



        firing_group = h5file["extracellular/electrode_1/firing"]

        try:
            firing_process_group = firing_group.create_group("processing")
        except ValueError:
            del h5file["extracellular/electrode_1/firing/processing"]
            firing_process_group = firing_group.create_group("processing")

        firing_origin = firing_group["origin_data"]

        phase_distrs_group = firing_process_group.create_group("phase_distrs")


        # тут нужно взять канал из пирамидного слоя
        band_pyr_channel = h5file["extracellular/electrode_1/lfp/processing/bands/channel_" + str(processing_param["number_pyr_layer"]) ]

        for celltype in firing_origin.keys():
            celltype_phase_distrs_group = phase_distrs_group.create_group(celltype)

            celltype_firings = np.empty(shape=0, dtype=np.float64)
            for dsetname, cell_firing_dset in firing_origin[celltype].items():
                celltype_firings = np.append(celltype_firings, cell_firing_dset[:])

            for band_name in processing_param["filt_bands"].keys():
                lfp_band = band_pyr_channel[band_name][:]
                bins, phase_distr, R = plib.get_phase_disrtibution(celltype_firings, lfp_band, fd)
                celltype_phase_distrs_group.create_dataset(band_name, data = phase_distr)

                ####################################################################################
                # save modulation (R) for all neurons
                celltype_phase_distrs_group.create_dataset(band_name + "_R", data = np.asarray(R) )



            ####################################################################################
            # phase precessions
        
        
    return
        
        
if __name__ == "__main__":
    from basic_parameters import basic_params
    
    filepath =  "/home/ivan/Data/CA1_simulation/artificial_signals.hdf5" # basic_params["file_results"] #
    # print(filepath)
    processing_and_save(filepath)






