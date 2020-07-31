from mpi4py import MPI
from neuron import h, load_mechanisms
from neuron.units import ms, mV
h.nrnmpi_init()


import numpy as np
import matplotlib.pyplot as plt
import h5py
import os
import sys

def join_lfp(comm, electrodes):
    rank = comm.Get_rank()

    lfp_data = []
    for el in electrodes:
        if el is None:
            sended = None
        else:
            sended = el.value
        reseved = comm.gather(sended, root=0)
        
        if rank == 0:
            lfp_el = []
            for var_tmp in reseved:
                if not var_tmp is None:
                    lfp_el.append(var_tmp) 
    
            lfp_el = np.vstack(lfp_el)
            lfp_el = np.sum(lfp_el, axis=0)
            
            lfp_data.append(lfp_el)
    
    return lfp_data

def join_vect_lists(comm, vect_list, gid_vect):
    
    jointed = []

    all_gid = comm.gather(gid_vect, root=0)

    for sp in vect_list:
        reseved = comm.gather(sp, root=0)
        if rank == 0:
            jointed.extend(reseved)
    
    if rank == 0:
        all_gid = np.hstack(all_gid).ravel()
        jointed = [x for _, x in sorted(zip(all_gid, jointed), key=lambda pair: pair[0])]
    return jointed




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
    
    soma_v_vecs = []
    
    
    for gid in gid_vect:
       
        if params["celltypes"][gid] == "pyr":
            cell = h.poolosyncell(gid, 0)
            
            is_pyrs_thread = True
            for sec in cell.all:
                pyramidal_sec_list.append(sec)
        
            pyr_coord_in_layer_x = radius_for_pyramids * 2 * (np.random.rand() - 0.5) # !!!! density of the pyramidal cells  
            pyr_coord_in_layer_y = radius_for_pyramids * 2 * (np.random.rand() - 0.5) # !!!! density of the pyramidal cells  

            cell.position(pyr_coord_in_layer_x, 0, pyr_coord_in_layer_y)
        
        elif params["celltypes"][gid] == "pvbas":
            cell = h.pvbasketcell(gid, 0)
        
        elif params["celltypes"][gid] == "olm":
            cell = h.olmcell(gid, 0)
        
        elif params["celltypes"][gid] == "cckbas":
            cell = h.cckcell(gid, 0)
        
        elif params["celltypes"][gid] == "ivy":
            cell = h.ivycell(gid, 0)
        
        elif params["celltypes"][gid] == "ngf":
            cell = h.ngfcell(gid, 0)
        
        elif params["celltypes"][gid] == "aac":
            cell = h.axoaxoniccell(gid, 0)
        
        elif params["celltypes"][gid] == "bis":
            cell= h.bistratifiedcell(gid, 0)
        
        elif params["celltypes"][gid] == "sca":
            cell = h.scacell(gid, 0)
        
        elif params["celltypes"][gid] == "ca3":
            cell = h.ArtifitialCell(gid, 0)
            cell.celltype = "ca3"
        
        elif params["celltypes"][gid] == "mec":
            cell = h.ArtifitialCell(gid, 0)
            cell.celltype = "mec"
        
        elif params["celltypes"][gid] == "lec":
            cell = h.ArtifitialCell(gid, 0)
            cell.celltype = "lec"
        
        elif params["celltypes"][gid] == "msteevracells":
            cell = h.ArtifitialCell(gid, 0)
            cell.celltype = "msteevracells"
        
        elif params["celltypes"][gid] == "mskomalicells":
            cell = h.ArtifitialCell(gid, 0)
            cell.celltype = "mskomalicells"
       
        pc.set_gid2node(gid, pc.id())
        
        # set counters for spike generation
        if cell.is_art() == 0:
            for sec in cell.all:
                sec.insert("IextNoise")
                sec.sigma_IextNoise = 0.0005
                sec.mean_IextNoise = 0.0005
            
            firing = h.NetCon(cell.soma[0](0.5)._ref_v, None, sec=cell.soma[0])
            firing.threshold = -40 * mV

        else:
            firing = h.NetCon(cell.acell, None)
        
        pc.cell(gid, firing)
        fring_vector = h.Vector()
        firing.record(fring_vector)
        spike_count_obj.append(firing)
        spike_times_vecs.append(fring_vector)
        
        
        # check is need to save Vm of soma
        if np.sum(params["save_soma_v"]["vect_idxes"] == gid) == 1:
            soma_v = h.Vector()
            soma_v.record(cell.soma[0](0.5)._ref_v)
            soma_v_vecs.append(soma_v)
        
        
        

        if cell.is_art() == 0:
            hh_cells.append(cell)
        
        all_cells.append(cell)


    
    
    # set connection
    connections = h.List()
    synapses = h.List()
    
    for pre_idx in range(ncells):
        
        for post_idx, postsynaptic_cell in enumerate(hh_cells):
            
            if pre_idx == postsynaptic_cell.gid:
                continue
                       
            try:
                
                conn_name = params["celltypes"][pre_idx] + "2" + postsynaptic_cell.celltype
                conn_data = params["connections"][conn_name]
                
            except AttributeError:
                continue
            except KeyError:
                continue

            

            if np.random.rand() > conn_data["prob"]:
                continue
            
            print(conn_name)
            
           
            
            post_comp = np.random.choice( getattr( postsynaptic_cell, conn_data["target_compartment"] ) )
            
            # print(post_comp)
             
            
            
            syn = h.Exp2Syn( post_comp(0.5) ) 
            syn.e = conn_data["Erev"]
            syn.tau1 = conn_data["tau_rise"]
            syn.tau2 = conn_data["tau_decay"]
            
            conn = pc.gid_connect(pre_idx, syn)
            
            # choce synaptic delay and weight from lognormal distribution 
            conn.delay = 0  # np.random.lognormal(mean=np.log(conn_data["delay"]), sigma=conn_data["delay_std"])   
            conn.weight[0] = conn_data["gmax"] # np.random.lognormal(mean=np.log(conn_data["gmax"]), sigma=conn_data["gmax_std"]) 

            
            connections.append(conn)
            synapses.append(syn)
            
    
        

    
    Nelecs = params["Nelecs"]
    el_x = np.zeros(Nelecs)
    el_y = np.linspace(-200, 1000, Nelecs)
    el_z = np.zeros(Nelecs)
    
    electrodes = []
    
    
    
    for idx_el in range(Nelecs):
        if is_pyrs_thread:
            le = LfpElectrode(x=el_x[idx_el], y=el_y[idx_el], z=el_z[idx_el], sampling_period=h.dt, sec_list=pyramidal_sec_list)
            electrodes.append(le)
        else:
            electrodes.append(None)
    

    soma1_v = None
    if pc.id() == 0 :
        print( len(hh_cells) )
        print( hh_cells[0].celltype )
        soma1_v = h.Vector()
        soma1_v.record(hh_cells[0].soma[0](0.5)._ref_v)

    if pc.id() == 0:
        t_sim = h.Vector()
        t_sim.record(h._ref_t)
    else:
        t_sim = None
        
    # h.tstop = 50 * ms
    
    pc.set_maxstep(10 * ms)
    h.finitialize(-64 * mV)
    # pc.barrier()
    pc.psolve(50 * ms)
    pc.barrier()
    
    print("Hello")
    if pc.id() == 0:
        soma1_v = np.asarray(soma1_v)
        # print(soma1_v)
        plt.plot(t, soma1_v)
        plt.savefig("../../Data/test.png")
        # plt.show()
    
    # unite data from all threads to 0 thread
    comm = MPI.COMM_WORLD
    
    lfp_data = join_lfp(comm, electrodes)
    spike_trains = join_vect_lists(comm, spike_times_vecs, gid_vect)
    soma_v_list = join_vect_lists(comm, soma_v_vecs, gid_vect)
    
    
    if (pc.id() == 0) and (params["file_results"] != None):
        with h5py.File(params["file_results"], 'w') as h5file:
            
            h5file.create_dataset("time", data = np.asarray(t_sim) )
            
            extracellular_group = h5file.create_group("extracellular")
            ele_group = extracellular_group.create_group('electrode_1')
            lfp_group = ele_group.create_group('lfp')
            
            lfp_group_origin = lfp_group.create_group('origin_data')
            lfp_group_origin.attrs['SamplingRate'] = 1000 / h.dt   # dt in ms 
            
            
            for idx_el, lfp in enumerate(lfp_data):
                lfp_group_origin.create_dataset("channel_" + str(idx_el+1), data = lfp)
            
            firing_group = h5file.create_group("extracellular/electrode_1/firing/origin_data")
            
            
            for celltype in set(params["celltypes"]):
                cell_friring_group = firing_group.create_group(celltype)
            
            
                for cell_idx, sp_times in enumerate(spike_trains):
                    if params["celltypes"][cell_idx] != celltype:
                        continue
                    
                    cell_spikes_dataset = cell_friring_group.create_dataset("neuron_" + str(cell_idx+1), data=sp_times)
            
    
    
            intracellular_group = h5file.create_group("intracellular")
            intracellular_group_origin = intracellular_group.create_group("origin_data")
            
            for v_idx, soma_v in enumerate(soma_v_vecs):
                soma_v_dataset = intracellular_group_origin.create_dataset("neuron_" + str(v_idx+1), data=soma_v)
                soma_v_dataset.attrs["celltype"] = params["celltypes"][params["save_soma_v"]["vect_idxes"][v_idx]]
    
 
    
        
    
    pc.done()
    h.quit()
    
    
    print("End of the simultion!")
    return
