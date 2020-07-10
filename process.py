import numpy as np
from elephant import signal_processing as sigp 
import matplotlib.pyplot as plt
import h5py

"""
t = np.linspace(0, 1, 1000)
s = np.cos(2 * np.pi * t * 5)

freqs = np.linspace(1, 20, 40)

W = sigp.wavelet_transform(s, freqs, nco=6.0, fs=1000)

W = np.abs(W)

plt.pcolor(t, freqs, W)

plt.show()
"""

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
    fd = lfp_group.attrs["SamplingRate"]
    
    lfp_keys = lfp_group.keys()
    
    for key_idx in range(len(lfp_keys)):
        key = "channel_" + str(key_idx + 1)
        lfp = lfp_group[key][:]
    
        freqs = np.fft.rfftfreq(lfp.size, d=1/fd)
        freqs = freqs[1:]  # remove 0 frequency
        freqs = freqs[freqs <= processing_param["max_freq_lfp"] ]  # remove frequencies below 500 Hz
        
        
               
        try:
            process_group = lfp_group.create_group(key + "_processing")
        except ValueError:
            del h5file["extracellular/electrode_1/lfp/" + key + "_processing"]
            process_group = lfp_group.create_group(key + "_processing")
            
        process_group.create_dataset("frequecies", data=freqs)
        wdset = process_group.create_dataset("wavelet_coeff", (len(freqs), len(lfp)), dtype="c16")
            
        for start_idx in range(0, freqs.size, processing_param["freqs_step"]):
            end_idx = start_idx + processing_param["freqs_step"]
            
            if end_idx > freqs.size:
                end_idx = freqs.size

            W = sigp.wavelet_transform(lfp, freqs[start_idx:end_idx], nco=processing_param["morlet_w0"], fs=fd)
            wdset[start_idx:end_idx, : ] = W
        
        
        for band_name, freq_lims in processing_param["filt_bands"].items():
            
            filtered_signal = sigp.butter(lfp, highpass_freq=freq_lims[1], \
                lowpass_freq=freq_lims[0], order= processing_param["butter_order"], fs=fd )
            
            
            process_group.create_dataset(band_name, data = filtered_signal)
            
            
        # начать от сюда !!!!!!!
        # 1. Создать набор данных правильного размера с правильным типом данных
        # 2. Сделать вейвлеты в цикле по freqs и сложить их в набор данных
        # 3. Сделать аналогично для фильтрованных сигналов в дельта, тета, гамма и риппл диапазонах !!!
        
        break



"""        
fig, axes = plt.subplots(nrows=len(lfp_keys))
    axes[key_idx].plot(t[1:-1], lfp_group[key][:], label=key )
    axes[key_idx].legend()
plt.show()
"""


