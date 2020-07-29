from mpi4py import MPI
from neuron import h, load_mechanisms
from neuron.units import ms, mV
h.nrnmpi_init()


import numpy as np
import matplotlib.pyplot as plt
import h5py
import os
import sys




def run_simulation(params):
    pc = h.ParallelContext()
    
   
    h.load_file("stdgui.hoc")
    h.load_file("import3d.hoc")
    load_mechanisms("./mods/")
    # h.cvode.use_fast_imem(1)

    sys.path.append("../LFPsimpy/")
    from LFPsimpy import LfpElectrode


    cell_path = "./cells/"
    for file in os.listdir(cell_path):
        if file.find(".hoc") != -1:
            h.load_file(cell_path + file)
    
    ncells = len(params["celltypes"])  # whole number of cells in the model
    gid_vect = np.arange( pc.id(), ncells, pc.nhost(), dtype=np.int )
    
    
    all_cells = h.List()
    hh_cells = h.List()
    artificial_cells = h.List()
    
    
    pyramidal_sec_list = h.SectionList()
    is_pyrs_thread = False
    radius_for_pyramids = np.sqrt( params["CellNumbers"]["Npyr"] / params["PyrDencity"] ) / np.pi 
    
    spike_count_obj = []
    spike_times_vecs = []
    
    
    for gid in gid_vect:
       
        if params["celltypes"][gid] == "pyr":
            cell_class = h.poolosyncell
        
        elif params["celltypes"][gid] == "pvbas":
            cell_class = h.pvbasketcell
        
        elif params["celltypes"][gid] == "olm":
            cell_class = h.olmcell
        
        elif params["celltypes"][gid] == "cckbas":
            cell_class = h.cckcell
        
        elif params["celltypes"][gid] == "ivy":
            cell_class = h.ivycell
        
        elif params["celltypes"][gid] == "ngf":
            cell_class = h.ngfcell
        
        elif params["celltypes"][gid] == "aac":
            cell_class = h.axoaxoniccell
        
        elif params["celltypes"][gid] == "bis":
            cell_class = h.bistratifiedcell
        
        elif params["celltypes"][gid] == "sca":
            cell_class = h.scacell
        
        elif params["celltypes"][gid] == "ca3":
            cell_class = h.ArtifitialCell
        
        elif params["celltypes"][gid] == "mec":
            cell_class = h.ArtifitialCell
        
        elif params["celltypes"][gid] == "lec":
            cell_class = h.ArtifitialCell
        
        elif params["celltypes"][gid] == "msteevracells":
            cell_class = h.ArtifitialCell
        
        elif params["celltypes"][gid] == "mskomalicells":
            cell_class = h.ArtifitialCell
       
       
        cell = cell_class(gid, 0)
        
        pc.set_gid2node(gid, pc.id())
        # print("hello")
        
        
        
        for sec in cell.all:
            sec.insert("IextNoise")
            sec.sigma_IextNoise = 0.0005
            sec.mean_IextNoise = 0.0005
        
        if params["celltypes"][gid] == "pyr":
            is_pyrs_thread = True
            for sec in cell.all:
                pyramidal_sec_list.append(sec)
        
            pyr_coord_in_layer_x = radius_for_pyramids * 2 * (np.random.rand() - 0.5) # !!!! density of the pyramidal cells  
            pyr_coord_in_layer_y = radius_for_pyramids * 2 * (np.random.rand() - 0.5) # !!!! density of the pyramidal cells  
        
        
            cell.position(pyr_coord_in_layer_x, 0, pyr_coord_in_layer_y) 
        
        hh_cells.append(cell)
        all_cells.append(cell)


    
    
    # set counters for spike generation
    list_of_celltypes = []
    for cell in hh_cells:
        firing = h.APCount(cell.soma[0](0.5))
        fring_vector = h.Vector()
        firing.record(fring_vector)
        spike_count_obj.append(firing)
        spike_times_vecs.append(fring_vector)
        list_of_celltypes.append(cell.celltype)

    """
    # set connection
    connections = h.List()
    synapses = h.List()
    
    for pre_idx, presynaptic_cell in enumerate(all_cells):
       
        for post_idx, postsynaptic_cell in enumerate(all_cells):
            
            if pre_idx == post_idx:
                continue
                       
            try:
                
                conn_name = presynaptic_cell.celltype + "2" + postsynaptic_cell.celltype
                conn_data = params[conn_name]
                
            except AttributeError:
                continue
            except KeyError:
                continue

            
            
            
            if np.random.rand() > conn_data["prob"]:
                continue
            
            print(conn_name)
            
            if presynaptic_cell.is_art() == 1:
                pre_comp = getattr( presynaptic_cell, conn_data["sourse_compartment"] )
            else:
                pre_comp = getattr( presynaptic_cell, conn_data["sourse_compartment"] )[-1]
            
            
            post_comp = np.random.choice( getattr( postsynaptic_cell, conn_data["target_compartment"] ) )
            
            # print(post_comp)
             
            
            
            syn = h.Exp2Syn( post_comp(0.5) ) 
            syn.e = conn_data["Erev"]
            syn.tau1 = conn_data["tau_rise"]
            syn.tau2 = conn_data["tau_decay"]
            
            if presynaptic_cell.is_art() == 1:
                conn = h.NetCon(pre_comp, syn, sec=post_comp)
            else:
                conn = h.NetCon(pre_comp(1.0)._ref_v, syn, sec=pre_comp) 
            
            
            # choce synaptic delay and weight from lognormal distribution 
            conn.delay = 0  # np.random.lognormal(mean=np.log(conn_data["delay"]), sigma=conn_data["delay_std"])   
            conn.weight[0] = conn_data["gmax"] # np.random.lognormal(mean=np.log(conn_data["gmax"]), sigma=conn_data["gmax_std"]) 

            connections.append(conn)
            synapses.append(syn)
            
        if (presynaptic_cell.is_art() == 1):
        
            fring_vector = h.Vector()
            conn.record(fring_vector)
            spike_times_vecs.append(fring_vector)
            list_of_celltypes.append(presynaptic_cell.celltype)
    """    
        

    
    Nelecs = params["Nelecs"]
    el_x = np.zeros(Nelecs)
    el_y = np.linspace(-200, 1000, Nelecs)
    el_z = np.zeros(Nelecs)
    
    electrodes = []
    
    if is_pyrs_thread:
    
        for idx_el in range(Nelecs):
            le = LfpElectrode(x=el_x[idx_el], y=el_y[idx_el], z=el_z[idx_el], sampling_period=h.dt, sec_list=pyramidal_sec_list)
            electrodes.append(le)
    else:
        le = None
    
    
   
    soma_v_vecs = []
    soma_v_cell_idx = []
    
    for cell_type, vect_of_idxes in params["save_soma_v"].items():
        
        for idx_v in vect_of_idxes:
            
            if np.sum(gid_vect == idx_v) == 0:
                continue
            
            indx_of_cells = int (idx_v % pc.nhost() )
                
            cell = all_cells[indx_of_cells]
            soma_v_cell_idx.append(indx_of_cells)
            if cell.celltype == cell_type:
            
                soma_v = h.Vector()
                soma_v.record(cell.soma[0](0.5)._ref_v)
                soma_v_vecs.append(soma_v)
        
        #print(cell_type)
        
    
    # print(len(soma_v_vecs))

    
   
    soma1_v = None
    if pc.id() == 0:
        print( len(hh_cells) )
        print( hh_cells[0].celltype )
        soma1_v = h.Vector()
        soma1_v.record(hh_cells[0].soma[0](0.5)._ref_v)


    t = h.Vector()
    t.record(h._ref_t)
    
    h.tstop = 50 * ms
    
    pc.set_maxstep(10 * ms)
    h.finitialize(-64 * mV)
    pc.barrier()
    pc.psolve(50 * ms)
    pc.barrier()
    
    print("Hello")
    if pc.id() == 0:
        soma1_v = np.asarray(soma1_v)
        # print(soma1_v)
        plt.plot(t, soma1_v)
        plt.savefig("../../Data/test.png")
        # plt.show()
    
    
    
    """
    if params["file_results"] != None:
        with h5py.File(params["file_results"], 'w') as h5file:
            
            h5file.create_dataset("time", data=t)
            
            extracellular_group = h5file.create_group("extracellular")
            ele_group = extracellular_group.create_group('electrode_1')
            lfp_group = ele_group.create_group('lfp')
            
            lfp_group_origin = lfp_group.create_group('origin_data')
            lfp_group_origin.attrs['SamplingRate'] = 1000 / h.dt   # dt in ms 
            
            
            for idx_el, el in enumerate(electrodes):
                lfp_group_origin.create_dataset("channel_" + str(idx_el+1), data = el.values)
            
    
            firing_group = h5file.create_group("extracellular/electrode_1/firing/origin_data")
            
            for celltype in params["celltypes"]:
                cell_friring_group = firing_group.create_group(celltype)
            
            
                for cell_idx, sp_times in enumerate(spike_times_vecs):
                    if list_of_celltypes[cell_idx] != celltype:
                        continue
                    
                    cell_spikes_dataset = cell_friring_group.create_dataset("neuron_" + str(cell_idx+1), data=sp_times)
                
    
    
            intracellular_group = h5file.create_group("intracellular")
            intracellular_group_origin = intracellular_group.create_group("origin_data")
            
            for v_idx, soma_v in enumerate(soma_v_vecs):
                soma_v_dataset = intracellular_group_origin.create_dataset("neuron_" + str(soma_v_cell_idx[v_idx]+1) , data=soma_v)
                soma_v_dataset.attrs["celltype"] = list_of_celltypes[soma_v_cell_idx[v_idx]]
    
 
    
        """
    
    pc.done()
    h.quit()
    
    
    print("End of the simultion!")
    return
