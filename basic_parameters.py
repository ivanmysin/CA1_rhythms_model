import numpy as np
import presimulation_lib as prelib

"""
pyr - CA1 piramidal cells
olm - Oriens-Lacunosum/Moleculare (OLM) Cells
pvbas - parvalbumin positive basket cells
cckbas - cholecystokinin positive basket cells
ivy - Ivy cells
ngf - neurogliaform cells
bis - bistratifered cells
aac - axo-axonal cells
csa - Schaffer collateral-associated cells


ca3 - CA3 pyramidal cells
mec - stellate cells of the medial entorhinal cortex
lec - FAN cells of the lateral entorhinal cortex


"""

Nelecs = 1 # number of electrodes

basic_params = {
    "elecs" : {
        "el_x" : np.zeros(Nelecs),
        "el_y" : np.zeros(Nelecs), # np.linspace(-200, 600, Nelecs),
        "el_z" : np.zeros(Nelecs),
    },
    "PyrDencity" : 0.2, # pyramidal cells / micrometer^2
    
    "file_results":  "../../Data/CA1_simulation/test.hdf5", # None, #
    "duration" : 1000, #  1400, # simulation time
    
    "del_start_time" : 400, # time after start for remove  
    
    "celltypes" : [],
    
    "CellNumbersInFullModel" : {
        "Npyr" :    9000,
        "Npvbas" : 200,
        "Nolm" :   80,
        "Ncckbas" : 160,
        "Nivy" :    260,
        "Nngf" :    130,
        "Nbis" :    70,
        "Naac" :    60,
        "Nsca" :    40,
        
        
        "Nca3" : 10000,
        "Nmec" : 10000, 
        "Nlec" : 10000,  
        "Nmsteevracells" : 200,
        "Nmskomalicells" : 200,
        "Nmsach"         : 50,
    },
    
    "CellNumbers" : {
        "Npyr" :    0, # 100, # 500,
        "Npvbas" :  100, # 100, # 100,
        "Nolm" :    0, #40,
        "Ncckbas" : 0, # 80, # 80
        "Nivy" :    0, #130,
        "Nngf" :    0, #65,
        "Nbis" :    0, #35,
        "Naac" :    0, #30,
        "Nsca" :    0, #20,
        
        
        "Nca3" : 500, #500,
        "Nmec" : 0, #500,
        "Nlec" : 0, #500,
        "Nmsteevracells" : 0, #200,
        "Nmskomalicells" : 0, # 200,
        "Nmsach"         : 0, #150,
    },
    
    "CellParameters" : {
        "ca3" : {
            "cellclass" : "ArtifitialCell",
            "R" : 0.4,
            "phase" : 1.5,
            "freqs" : 5.0,
            "latency" : 10.0,
            "spike_train_freq" : 5.0,      
        },
        
        "mec" : {
            "cellclass" : "ArtifitialCell",
            "R" : 0.4,
            "phase" : 0.0,
            "freqs" : 5.0,
            "latency" : 10.0,
            "spike_train_freq" : 5.0,    
        },
        
        "lec" : {
            "cellclass" : "ArtifitialCell",
            "R" : 0.1,
            "phase" : 0.0,
            "freqs" : 5.0,
            "latency" : 10.0,
            "spike_train_freq" : 5.0,      
        },
        
        "msteevracells" : {
            "cellclass" : "ArtifitialCell",
            "R" : 0.8,
            "phase" : np.pi,
            "freqs" : 5.0,
            "latency" : 4.0,
            "spike_train_freq" : 15.0,      
        },
        
        "mskomalicells" : {
            "cellclass" : "ArtifitialCell",
            "R" : 0.8,
            "phase" : 0.0,  # !!!!
            "freqs" : 5.0,
            "latency" : 4.0,
            "spike_train_freq" : 15.0,      
        },
        
        "msach" : {
            "cellclass" : "ArtifitialCell",
            "R" : 0.6,
            "phase" : np.pi,  # !!!!
            "freqs" : 5.0,
            "latency" : 10.0,
            "spike_train_freq" : 10.0,      
        },
        
        "pyr" : {
            "cellclass" : "CA1PyramidalCell", # "poolosyncell", # 
            "iext" : 0.0, # 0.002,
            "iext_std" : 0.002,
        },
        
        "pvbas" : {
            "cellclass" : "pvbasketcell",
            "iext" : 0.0,
            "iext_std" : 0.0,
        },
        
        "cckbas" : {
            "cellclass" : "cckcell",
            "iext" : 0.002, #!!! 0.003,
            "iext_std" : 0.003,
        },

        "olm" : {
            "cellclass" : "olmcell",
            "iext" : 0.0,
            "iext_std" : 0.002,
        },
        
        "aac" : {
            "cellclass" : "axoaxoniccell",
            "iext" : 0.0,
            "iext_std" : 0.002,
        },
        
        "ngf" : {
            "cellclass" : "ngfcell",
            "iext" : 0.001,
            "iext_std" : 0.002,
        },
        
        "ivy" : {
            "cellclass" : "ivycell",
            "iext" : 0.001,
            "iext_std" : 0.002,
        },
    
        "bis" : {
            "cellclass" : "CA1BistratifiedCell", # "bistratifiedcell",
            "iext" : 0.005,
            "iext_std" : 0.002,
        },
        
        "sca" : {
            "cellclass" : "scacell",
            "iext" : 0.001,
            "iext_std" : 0.002,
        },
    
    },
    
    "save_soma_v" : {
        "pyr" :  [range(100)],    # [0, ],
        "pvbas" : [range(20, 31)], #
        "olm" : [0, ],
        "cckbas" : [0, ],
        "ivy" : [0, ],
        "ngf" : [0, ],
        "bis" : [0, ],
        "aac" : [0, ],
        "sca" : [0, ],
    
        "vect_idxes" : [],
    
    },


    "connections" : {
        
        # connection to pyramidal neurons
        "ca32pyr": {
            "gmax": 0.09, # 0.016,
            "gmax_std" : 0.002,
            
            "Erev": 0,
            "tau_rise": 0.5,
            "tau_decay": 3,

            "prob": 0.06,
            
            "delay": 1.5,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "rad_list",
        },
        
       "mec2pyr": {
            "gmax": 0.06,
            "gmax_std" : 0.007,
            
            "Erev": 0,
            "tau_rise": 0.5,
            "tau_decay": 3,

            "prob": 0.07,
            
            "delay": 10,
            "delay_std" : 2,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "lm_list",
        },
        
        "lec2pyr": {  # need to optimize
            "gmax": 0.06,
            "gmax_std" : 0.007,
            
            "Erev": 0,
            "tau_rise": 0.5,
            "tau_decay": 3,

            "prob": 0.07,
            
            "delay": 10,
            "delay_std" : 2,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "lm_list",
        },
        

        "pyr2pyr": {
            "gmax": 0.01,
            "gmax_std" : 0.007,

            "Erev": 0.0,
            "tau_rise": 0.1,
            "tau_decay": 1.5,

            "prob": 0.009,

            "delay": 1.2,
            "delay_std" : 0.2,


            "sourse_compartment" : "axon",
            "target_compartment" : "basal_list",
        },
        
        "cckbas2pyr": {
            "gmax": 2.5,
            "gmax_std" : 1.2,
            
            "Erev": -75,
            "tau_rise": 0.2,
            "tau_decay": 4.2,

            "prob": 0.63,
            
            "delay": 2.5,
            "delay_std" : 1.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "soma_list",
        },

      
       "ivy2pyr": {
            "gmax": 0.053,
            "gmax_std" : 0.02,
            
            "Erev": -75,
            "tau_rise": 1.1,
            "tau_decay": 11,

            "prob": 0.13,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "lm_list",
        },
        
        
       "aac2pyr": {
            "gmax": 20.5,
            "gmax_std" : 10,

            "Erev": -75,
            "tau_rise": 0.28,
            "tau_decay": 8.4,

            "prob": 0.29,

            "delay": 1.2,
            "delay_std" : 0.2,


            "sourse_compartment" : "soma",
            "target_compartment" : "axon_list",
        },
        
       "olm2pyr": {
            "gmax": 1.7,
            "gmax_std" : 0.9,
            
            "Erev": -75,
            "tau_rise": 0.13,
            "tau_decay": 11,

            "prob": 0.29,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "lm_list",
        },
        
       "pvbas2pyr": {
            "gmax": 0.05,
            "gmax_std" : 0.025,
            
            "Erev": -75,
            "tau_rise": 0.3,
            "tau_decay": 6.2,

            "prob": 0.29,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "soma_list",
        },
        
       "bis2pyr": {
            "gmax": 0.009,
            "gmax_std" : 0.005,

            "Erev": -75,
            "tau_rise": 0.11,
            "tau_decay": 9.7,

            "prob": 0.14,

            "delay": 1.2,
            "delay_std" : 0.2,


            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },

       "ngf2pyr": {
            "gmax": 0.098,
            "gmax_std" : 0.05,

            "Erev": -75,
            "tau_rise": 9,
            "tau_decay": 39,

            "prob": 0.29,

            "delay": 1.2,
            "delay_std" : 0.2,


            "sourse_compartment" : "soma",
            "target_compartment" : "lm_list",
        },

       "sca2pyr": {
            "gmax": 0.098,
            "gmax_std" : 0.05,

            "Erev": -75,
            "tau_rise": 0.3,
            "tau_decay": 6.2,

            "prob": 0.29,

            "delay": 1.2,
            "delay_std" : 0.2,


            "sourse_compartment" : "soma",
            "target_compartment" : "rad_list",
        },
        # end connection to pyramids
        
        # connection to pvbas
        "ca32pvbas": {
            "gmax": 0.7, # 0.7,
            "gmax_std" : 0.2,
            
            "Erev": 0,
            "tau_rise": 2.0,
            "tau_decay": 6.3,

            "prob": 0.2, # 0.02,
            
            "delay": 1.5,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "dendrite_list",
        },
        
        "pyr2pvbas": {
            "gmax": 5, # !!!! 0.05,
            "gmax_std" : 0.04,
            
            "Erev": 0,
            "tau_rise": 0.07,
            "tau_decay": 0.2,

            "prob": 1, # 0.13,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "axon",
            "target_compartment" : "dendrite_list",
        },
        
        "pvbas2pvbas": {
            "gmax": 10, # 0.08, # 0.05 !!!! 0.023,
            "gmax_std" : 0.01, #  0.01,
            
            "Erev": -75,
            "tau_rise": 0.8,
            "tau_decay": 4.8,

            "prob": 0.7,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "soma", # "dendrite_list",
        },
        
        "cckbas2pvbas": {
            "gmax": 1.5, #!!! 1.0,
            "gmax_std" : 0.2,
            
            "Erev": -75,
            "tau_rise": 0.43,
            "tau_decay": 4.49,

            "prob": 0.38,
            
            "delay": 4.5,
            "delay_std" : 2.0,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "soma",
        },
        
        "olm2pvbas": {
            "gmax": 0.73,
            "gmax_std" : 0.35,
            
            "Erev": -75,
            "tau_rise": 0.25,
            "tau_decay": 7.5,

            "prob": 0.2, # optimized
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        # hypotetical connections
        "bis2pvbas": {
            "gmax": 0.1,
            "gmax_std" : 0.05,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.2, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        # "ngf2pvbas": {
        #     "gmax": 0.1,
        #     "gmax_std" : 0.05,
        #
        #     "Erev": -75,
        #     "tau_rise": 0.5,
        #     "tau_decay": 4.0,
        #
        #     "prob": 0.2,
        #
        #     "delay": 1.2,
        #     "delay_std" : 0.2,
        #
        #
        #     "sourse_compartment" : "soma",
        #     "target_compartment" : "dendrite_list",
        # },
        
        "ivy2pvbas": {
            "gmax": 1.1,
            "gmax_std" : 0.5,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.2, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "soma",
        },
        
        # "sca2pvbas": {
        #     "gmax": 0.1,
        #     "gmax_std" : 0.05,
        #
        #     "Erev": -75,
        #     "tau_rise": 0.5,
        #     "tau_decay": 4.0,
        #
        #     "prob": 0.1,
        #
        #     "delay": 1.2,
        #     "delay_std" : 0.2,
        #
        #
        #     "sourse_compartment" : "soma",
        #     "target_compartment" : "dendrite_list",
        # },
        
        # end connection to pvbas
        
        # connections to cckbas
        "msteevracells2cckbas" : {
            "gmax" : 1.5, # !!!! 
            "gmax_std" : 0.7, # !!!!
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 5.0,
            
            "prob": 0.5,
            
            "delay": 10.5,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "soma",
        },
        
        "pvbas2cckbas": {
            "gmax": 1.0,
            "gmax_std" : 0.2,
            
            "Erev": -75,
            "tau_rise": 0.29,
            "tau_decay": 2.67,

            "prob": 0.15,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
       
       "cckbas2cckbas": {
            "gmax": 1.0, #  1.0,
            "gmax_std" : 0.2, # 0.2
            
            "Erev": -75,
            "tau_rise": 0.2,
            "tau_decay": 4.2,

            "prob": 0.63,
            
            "delay": 2.7,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        
        # hypotetical connections
        "olm2cckbas": {
            "gmax": 1.5,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.2, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "bis2cckbas": {
            "gmax": 1.5,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.2, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        # "ngf2cckbas": {
        #     "gmax": 1.5,
        #     "gmax_std" : 0.7,
        #
        #     "Erev": -75,
        #     "tau_rise": 0.5,
        #     "tau_decay": 4.0,
        #
        #     "prob": 0.2,
        #
        #     "delay": 1.2,
        #     "delay_std" : 0.2,
        #
        #
        #     "sourse_compartment" : "soma",
        #     "target_compartment" : "dendrite_list",
        # },
        
        # "ivy2cckbas": {
        #     "gmax": 0.5,
        #     "gmax_std" : 0.2,
        #
        #     "Erev": -75,
        #     "tau_rise": 0.5,
        #     "tau_decay": 4.0,
        #
        #     "prob": 0.2,
        #
        #     "delay": 1.2,
        #     "delay_std" : 0.2,
        #
        #
        #     "sourse_compartment" : "soma",
        #     "target_compartment" : "dendrite_list",
        # },
        #
        # end connections to cckbas
        
        
        # connections to aac
        "msteevracells2aac" : {
            "gmax" : 1.5, # !!!! 
            "gmax_std" : 0.7, # !!!!
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 3,
            
            "prob": 0.5,
            
            "delay": 10.5,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "soma",
        },
        
        "pyr2aac": {
            "gmax": 0.04,
            "gmax_std" : 0.02,
            
            "Erev": 0,
            "tau_rise": 0.3,
            "tau_decay": 0.6,

            "prob": 0.07,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "axon",
            "target_compartment" : "dendrite_list",
        },
        
        "ca32aac": {
            "gmax": 0.7,
            "gmax_std" : 0.2,
            
            "Erev": 0,
            "tau_rise": 2,
            "tau_decay": 6.3,

            "prob": 0.01,
            
            "delay": 2.5,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "dendrite_list",
        },
        
        
        # hypotetical connections
        "mec2aac": {
            "gmax": 0.1,
            "gmax_std" : 0.05,
            
            "Erev": 0,
            "tau_rise": 2,
            "tau_decay": 6.3,

            "prob": 0.06,
            
            "delay": 8.0,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "dendrite_list",
        },
        
        "lec2aac": {
            "gmax": 0.1,
            "gmax_std" : 0.05,
            
            "Erev": 0,
            "tau_rise": 2,
            "tau_decay": 6.3,

            "prob": 0.003,
            
            "delay": 8.0,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "dendrite_list",
        },
        
        "olm2aac": {
            "gmax": 1.5,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.2, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "bis2aac": {
            "gmax": 1.5,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.2, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "pvbas2aac": {
            "gmax": 1.5,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.2, # 0.8, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "cckbas2aac": {
            "gmax": 1.5,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.2, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "ivy2aac": {
            "gmax": 1.5,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.2, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "sca2aac": {
            "gmax": 1.5,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.1, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        # end connections to aac
        
        # connections to olm
        "msach2olm" : {
            "gmax" : 0.5, 
            "gmax_std" : 0.1,
            "Erev": 0,
            "tau_rise": 0.5,
            "tau_decay": 3,
            
            "prob": 0.4,
            
            "delay": 10.5,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "soma",
        },

       "pyr2olm": {
            "gmax": 0.031,
            "gmax_std" : 0.0015,
            
            "Erev": 0,
            "tau_rise": 0.3,
            "tau_decay": 0.6,

            "prob": 0.081,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "axon",
            "target_compartment" : "soma",
        },
       
       
       # hypotetical connections
       "ivy2olm": {
            "gmax": 1.5,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.2, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
       
       "sca2olm": {
            "gmax": 1.5,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.2, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        # end connections to olm
        
        # connections to bis
       "pyr2bis": {
            "gmax": 0.14,
            "gmax_std" : 0.07,
            
            "Erev": 0,
            "tau_rise": 1.3,
            "tau_decay": 8.0,

            "prob": 0.14,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "axon",
            "target_compartment" : "dendrite_list",
        },
        
       "pvbas2bis": {
            "gmax": 0.035,
            "gmax_std" : 0.015,
            
            "Erev": -75,
            "tau_rise": 0.29,
            "tau_decay": 2.67,

            "prob": 0.2,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "cckbas2bis": {
            "gmax": 0.5,
            "gmax_std" : 0.2,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.2,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "sca2bis": {
            "gmax": 0.5,
            "gmax_std" : 0.2,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.05,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        # hypotetical connetions to bis
        
        
        # end connections to bis
        "bis2bis": {
            "gmax": 0.5,
            "gmax_std" : 0.2,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.5, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        # connections to ivy    
       "pyr2ivy": {
            "gmax": 0.041,
            "gmax_std" : 0.021,
            
            "Erev": 0,
            "tau_rise": 0.3,
            "tau_decay": 0.6,

            "prob": 0.13,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "axon",
            "target_compartment" : "dendrite_list",
        },
        
        # hypotetical connections
        "ivy2ivy": {
            "gmax": 0.5,
            "gmax_std" : 0.2,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.5, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },

        "pvbas2ivy": {
            "gmax": 1.5,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.5, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },

        "cckbas2ivy": {
            "gmax": 0.5,
            "gmax_std" : 0.07,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0, # !!!! 0.1, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "sca2ivy": {
            "gmax": 1.5,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.1, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
         # end connections to ivy
        
       
        # connections to ngf
        "ca32nfg": {
            "gmax": 1.42,
            "gmax_std" : 0.6 ,
            
            "Erev": 0,
            "tau_rise": 0.5,
            "tau_decay": 3,

            "prob": 0.05, #!! 0.1,
            
            "delay": 1.5,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "dendrite_list",
        },
        
        "mec2ngf": {
            "gmax": 0.7,
            "gmax_std" : 0.3,
            
            "Erev": 0,
            "tau_rise": 0.5,
            "tau_decay": 3,

            "prob": 0.1, # ! need to optimize
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "dendrite_list",
        },
        
        "lec2ngf": {
            "gmax": 0.7,
            "gmax_std" : 0.3,
            
            "Erev": 0,
            "tau_rise": 0.5,
            "tau_decay": 3,

            "prob": 0.05, # ! need to optimize
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "dendrite_list",
        },
        
        "olm2ngf": {
            "gmax": 2.5, #!! 1.27,
            "gmax_std" : 0.6,
            
            "Erev": -75,
            "tau_rise": 1.3,
            "tau_decay": 10.2,

            "prob": 0.2,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
       "ngf2ngf": {
            "gmax": 0.75,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 3.1,
            "tau_decay": 42,

            "prob": 0.7,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
 
        # no hypotetical connections
        # end of connections to ngf
        
        
        # connections to sca
       "olm2sca": {
            "gmax": 1.3,
            "gmax_std" : 0.6,
            
            "Erev": -75,
            "tau_rise": 0.07,
            "tau_decay": 29,

            "prob": 0.1,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        

       "sca2sca": {
            "gmax": 0.03,
            "gmax_std" : 0.015,
            
            "Erev": -75,
            "tau_rise": 4 ,
            "tau_decay": 34.3,

            "prob": 0.3,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        # hypotetical connections
        "ca32sca": {
            "gmax": 0.05,
            "gmax_std" : 0.02,
            
            "Erev": 0,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.09, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "dendrite_list",
        },
        
        "ivy2sca": {
            "gmax": 0.5,
            "gmax_std" : 0.2,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.1, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "ngf2sca": {
            "gmax": 0.5,
            "gmax_std" : 0.2,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.2, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "bis2sca": {
            "gmax": 0.5,
            "gmax_std" : 0.2,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.1, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
  

    }, # end of connetion settings

}


cell_types_in_model = []
gids_of_celltypes = {}

for celltype, numbers in sorted(basic_params["CellNumbers"].items()):
    
    celltype = celltype[1:]
    
    start_idx = len(cell_types_in_model)
    
    cell_types_in_model.extend( [celltype, ] * numbers )
    
    end_idx = len(cell_types_in_model)
    gids_of_celltypes[celltype] = np.arange(start_idx, end_idx)
    
    

basic_params["celltypes"] = cell_types_in_model

# print(basic_params["celltypes"])

save_soma_v_idx = np.empty(shape=0, dtype=np.int)

for celltype, list_idx in basic_params["save_soma_v"].items():

    
    if celltype == "vect_idxes": continue

    # list_idx = np.arange(basic_params["CellNumbers"]["N"+celltype] )
    
    indices = [i for i, x in enumerate(basic_params["celltypes"]) if x == celltype]
    if len(indices) == 0:
        continue

    indices = np.asarray(indices)
    list_idx = np.asarray(list_idx)
    
    save_soma_v_idx = np.append(save_soma_v_idx, indices[list_idx])



#for idx in save_soma_v_idx:
#    print(basic_params["celltypes"][idx])


basic_params["save_soma_v"]["vect_idxes"] = save_soma_v_idx

for celltypename, cellparam in basic_params["CellParameters"].items():
    try:
        Rgen = cellparam["R"]
        kappa, I0 = prelib.r2kappa(Rgen)
        cellparam["kappa"] = kappa
        cellparam["I0"] = I0
    
    except KeyError:
        continue


synapses = []

Npyr = gids_of_celltypes["pyr"].size
Npvbas = gids_of_celltypes["pvbas"].size
Nca3 = gids_of_celltypes["ca3"].size

pyr_coord_x =  np.zeros( Npyr,  dtype=np.float) # np.linspace(0, 1, Npyr)
pyr_coord_x[20:30] = 0.5

pvbas_coord_x = np.zeros( Npvbas,  dtype=np.float)  # np.linspace(0, 1, Npvbas)
pvbas_coord_x[20:30] = 0.5

ca3_coord_x = np.zeros( Nca3,  dtype=np.float) + 0.5


NNN = len( basic_params["celltypes"] )
# print(NNN)


# Wpyrbas = np.zeros( [NNN, NNN],  dtype=np.float)


for presynaptic_cell_idx, pre_celltype in enumerate(basic_params["celltypes"]):
    for postsynaptic_cell_idx, post_celltype in enumerate(basic_params["celltypes"]):
        dist_normalizer = 0


        if presynaptic_cell_idx == postsynaptic_cell_idx: continue

        try:
            conn_name = pre_celltype + "2" + post_celltype
            conn_data = basic_params["connections"][conn_name]
                
        except AttributeError:
            continue
        except KeyError:
            continue
        
        number_connections = int( np.floor(conn_data["prob"]) )
        if (np.random.rand() < (conn_data["prob"] - number_connections) ):
            number_connections += 1

        gmax = conn_data["gmax"]

        if conn_name == "ca32pyr":
            pyr_idx = postsynaptic_cell_idx - gids_of_celltypes["pyr"][0]
            ca3_idx = presynaptic_cell_idx - gids_of_celltypes["ca3"][0]
            dist = pyr_coord_x[pyr_idx] - ca3_coord_x[ca3_idx]
            dist_normalizer = np.exp(-0.5 * dist**2 / 0.2)

            # Wpyrbas[presynaptic_cell_idx, postsynaptic_cell_idx] = dist_normalizer
            # medium_pyr_idx = gids_of_celltypes["pyr"][gids_of_celltypes["pyr"].size // 2]
            # dist_normalizer = np.exp(-0.5 * (postsynaptic_cell_idx - medium_pyr_idx) ** 2 / 50)

            if dist_normalizer > 0.7:
                number_connections += 1
                gmax = 3

        elif conn_name == "pyr2pyr":
            pyr_idx1 = postsynaptic_cell_idx - gids_of_celltypes["pyr"][0]
            pyr_idx2 = presynaptic_cell_idx - gids_of_celltypes["pyr"][0]
            dist = pyr_coord_x[pyr_idx1] - pyr_coord_x[pyr_idx2]
            dist_normalizer = np.exp(-0.5 * dist**2 / 0.2)

            # Wpyrbas[presynaptic_cell_idx, postsynaptic_cell_idx] = dist_normalizer
            if dist_normalizer > 0.7:
                number_connections += 1
                gmax = 1.5
            else:
                number_connections = 0

        elif conn_name == "pvbas2pyr":
            pyr_idx = postsynaptic_cell_idx - gids_of_celltypes["pyr"][0]
            pvbas_idx = presynaptic_cell_idx - gids_of_celltypes["pvbas"][0]
            dist = pyr_coord_x[pyr_idx] - pvbas_coord_x[pvbas_idx]
            dist_normalizer = np.exp(-0.5 * dist**2 / 0.2)

            # Wpyrbas[presynaptic_cell_idx, postsynaptic_cell_idx] = dist_normalizer


            if dist_normalizer > 0.7:
                number_connections += 1
                gmax = 50
            else:
                number_connections = 0

        elif conn_name == "pyr2pvbas":
            pyr_idx = presynaptic_cell_idx - gids_of_celltypes["pyr"][0]
            pvbas_idx = postsynaptic_cell_idx - gids_of_celltypes["pvbas"][0]
            dist = pyr_coord_x[pyr_idx] - pvbas_coord_x[pvbas_idx]
            dist_normalizer = np.exp(-0.5 * dist**2 / 0.2)

            # Wpyrbas[presynaptic_cell_idx, postsynaptic_cell_idx] = dist_normalizer

            if dist_normalizer > 0.7:
                number_connections += 1
                gmax = 2
            else:
                number_connections = 0


        elif conn_name == "ca32pvbas":
            # medium_pvbas_idx = gids_of_celltypes["pyr"][gids_of_celltypes["pyr"].size // 2]
            # dist_normalizer_pvbas = np.exp(-0.5 * (postsynaptic_cell_idx - medium_pvbas_idx) ** 2 / 50)
            pvbas_idx = postsynaptic_cell_idx - gids_of_celltypes["pvbas"][0]
            ca3_idx = presynaptic_cell_idx - gids_of_celltypes["ca3"][0]

            dist = pvbas_coord_x[pvbas_idx] - ca3_coord_x[ca3_idx]
            dist_normalizer = np.exp(-0.5 * dist**2 / 0.2)

            # Wpyrbas[presynaptic_cell_idx, postsynaptic_cell_idx] = dist_normalizer
            if dist_normalizer > 0.7:
                number_connections += 1
                gmax = 0.3
            else:
                number_connections = 0

        elif conn_name == "pvbas2pvbas":
            pvbas_idx1 = postsynaptic_cell_idx - gids_of_celltypes["pvbas"][0]
            pvbas_idx2 = presynaptic_cell_idx - gids_of_celltypes["pvbas"][0]
            dist = pvbas_coord_x[pvbas_idx1] - pvbas_coord_x[pvbas_idx2]

            # Wpyrbas[presynaptic_cell_idx, postsynaptic_cell_idx] = dist_normalizer
            dist_normalizer = np.exp(-0.5 * dist**2 / 0.2)
            if dist_normalizer > 0.7:
                number_connections += 1
                gmax = 1.0 # 500
            else:
                number_connections = 0


        # Wpyrbas[presynaptic_cell_idx, postsynaptic_cell_idx] = dist_normalizer

        for _ in range(number_connections):
            
            delay = np.random.lognormal(mean=np.log(conn_data["delay"]), sigma=conn_data["delay_std"]) 
            if delay <= 0.5:
                delay = 0.5
            
            gmax_syn =  np.random.lognormal(mean=np.log(gmax), sigma=conn_data["gmax_std"])


            if gmax_syn < 0.000001: # or gmax_syn > 50:
                continue


            connection = {
                "pre_gid" : presynaptic_cell_idx,
                "post_gid" : postsynaptic_cell_idx,
                
                "gmax" : gmax_syn,
                "Erev" : conn_data["Erev"],
                "tau_rise" : conn_data["tau_rise"],
                "tau_decay" : conn_data["tau_decay"],
                "delay" : delay,
                
                "sourse_compartment" : conn_data["sourse_compartment"],
                "target_compartment" : conn_data["target_compartment"],

            }
            
            synapses.append(connection)


for syn in synapses:
    syn["gmax"] *= 0.001  # recalulate nS to micromhos
    # conn_data["gmax_std"] *= 0.001
    syn["delay"] += 1.5  # add delay on spike generation

    # print(conname)
    # precell, postcell = conname.split("2")

    # try:
    #     conn_data["prob"] = conn_data["prob"] * basic_params["CellNumbersInFullModel"]["N"+precell] / basic_params["CellNumbers"]["N"+precell]
    # except ZeroDivisionError:
    #     conn_data["prob"] = 0


#print(len(synapses))
basic_params["synapses_params"] = synapses


# import matplotlib.pyplot as plt
#
# plt.imshow(Wpyrbas)
# plt.show()




























