import numpy as np
from elephant import signal_processing as sigp 
import matplotlib.pyplot as plt
import h5py
import processingLib as plib



processing_param = {

    "morlet_w0" : 6.0,     # центральная частота для вейвлета Морле
    "freqs_step" : 10,     # количество частот, для которых вычисляется вейвлет за один цикл 
    "max_freq_lfp" : 500,  # Гц, анализируем только до этой частоты 

    "butter_order" : 4,    # Порядок для фильтра Баттерворда
    "filt_bands" : {
        "delta" : [1, 4], 
        "theta" : [4, 12], 
        "slow gamma" : [25, 50], 
        "fast gamma" : [50, 120], 
        "slow ripples" : [80, 250], 
        "fast ripples" : [200, 500], 
   
    },

}


filepath = "/home/ivan/Data/CA1_simulation/test.hdf5"

with h5py.File(filepath, 'a') as h5file:
    t = h5file["time"][:]
        
    lfp_group = h5file["extracellular/electrode_1/lfp"]
    lfp_group_origin = lfp_group["origin_data"]
    
    try:
        process_group = lfp_group.create_group("processing")
    except ValueError:
        del h5file["extracellular/electrode_1/lfp/processing"]
        process_group = lfp_group.create_group("processing")
    
    
    fd = lfp_group_origin.attrs["SamplingRate"]
    lfp_keys = lfp_group_origin.keys()
    
    for key_idx in range(len(lfp_keys)):
        key = "channel_" + str(key_idx + 1)
        lfp = lfp_group_origin[key][:]
    
        freqs = np.fft.rfftfreq(lfp.size, d=1/fd)
        freqs = freqs[1:]  # remove 0 frequency
        freqs = freqs[freqs <= processing_param["max_freq_lfp"] ]  # remove frequencies below 500 Hz
   
   
        wavelet_group = process_group.create_group(key + "_wavelet")
        
        wavelet_group.create_dataset("frequecies", data=freqs)
        wdset = wavelet_group.create_dataset(key + "wavelet_coeff", (len(freqs), len(lfp)), dtype="c16")
            
        for start_idx in range(0, freqs.size, processing_param["freqs_step"]):
            end_idx = start_idx + processing_param["freqs_step"]
            
            if end_idx > freqs.size:
                end_idx = freqs.size

            W = sigp.wavelet_transform(lfp, freqs[start_idx:end_idx], nco=processing_param["morlet_w0"], fs=fd)
            wdset[start_idx:end_idx, : ] = W
        
        bands_group = process_group.create_group(key + "_bands")
        for band_name, freq_lims in processing_param["filt_bands"].items():
            
            filtered_signal = sigp.butter(lfp, highpass_freq=freq_lims[1], \
                lowpass_freq=freq_lims[0], order= processing_param["butter_order"], fs=fd )
            
            bands_group.create_dataset(band_name, data = filtered_signal)
            
        
        
       
        break
    
    firing_group = h5file["extracellular/electrode_1/firing"]
    
    try:
        # тут можно сделать цикл по ритмам, пока берем только тета 
        firing_process_group = firing_group.create_group("processing")
    except ValueError:
        del h5file["extracellular/electrode_1/firing/processing"]
        firing_process_group = firing_group.create_group("processing")
    
    firing_origin = firing_group["origin_data"]
    
    firing_theta = firing_process_group.create_group("theta")
    
    # print( firing_origin.keys() )
    
    for celltype in firing_origin.keys():
        
        celltype_firings = np.empty(shape=0, dtype=np.float64)
       
        for dsetname, cell_firing_dset in firing_origin[celltype].items():

            celltype_firings = np.append(celltype_firings, cell_firing_dset[:])
        
         # тут нужно взять канал из пирамидного слоя
        theta_lfp = h5file["extracellular/electrode_1/lfp/processing/channel_1_bands/theta"][:]
        bins, phase_distr = plib.get_phase_disrtibution(celltype_firings, theta_lfp, fd)
        
        
        firing_theta.create_dataset(celltype, data = phase_distr)
        
        

        
        
        
    
    






