import numpy as np
import matplotlib.pyplot as plt
import h5py


def plot_v(filepath):
    
    with h5py.File(filepath, 'r') as h5file:
        t = h5file["time"][:]
        
        intracellular_group = h5file["intracellular"]
        
        intracell_keys = intracellular_group.keys()
        
        
        fig, axes = plt.subplots(nrows=len(intracell_keys))
        
        for idx, key in enumerate(intracell_keys):
            v = intracellular_group[key][:]
        
            axes[idx].plot(t, v, label = intracellular_group[key].attrs["celltype"] )
            axes[idx].legend()
            
        plt.show()


def plot_spike_raster(filepath):
    
    with h5py.File(filepath, 'r') as h5file:
        raster_group = h5file["spike_raster"]
        spikes_keys = raster_group.keys()
        
        celltypes = [raster_group[key].attrs["celltype"]  for key in  spikes_keys   ]
        uniq_celltypes = list(set(celltypes))
        
        fig, axes = plt.subplots(nrows=len(uniq_celltypes))
        
        
        
        for sp_idx, key in enumerate(spikes_keys):
            
            firing = raster_group[key][:]
            
            # print(raster_group[key].attrs)
            
            
            celltype_idx = uniq_celltypes.index(raster_group[key].attrs["celltype"])
            
            axes[celltype_idx].scatter(firing,  np.zeros(firing.size) + sp_idx + 1, color="b", s=1 )
        
        
        
        for celltype_idx, celltype in enumerate(uniq_celltypes):
            axes[celltype_idx].set_title(celltype)
        
        
        plt.show()


def plot_lfp(filepath):
    with h5py.File(filepath, 'r') as h5file:
        t = h5file["time"][:]
        
        lfp_group = h5file["extracellular/electrode_1/lfp"]
        fd = lfp_group.attrs["SamplingRate"]
        lfp_keys = lfp_group.keys()
        
        fig, axes = plt.subplots(nrows=len(lfp_keys))
        
        for key_idx in range(len(lfp_keys)):
            key = "channel_" + str(key_idx + 1)
            axes[key_idx].plot(t[1:-1], lfp_group[key][:], label=key )
            axes[key_idx].legend()
        
        
        plt.show()



path = "/home/ivan/Data/CA1_simulation/test.hdf5"

# plot_v(path)
# plot_spike_raster(path)
plot_lfp(path)
