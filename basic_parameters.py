import numpy as np
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


basic_params = {
    "Nelecs" : 3,      # number of electrodes
    "PyrDencity" : 0.2, # pyramidal cells / micrometer^2
    
    "file_results":  "../../Data/CA1_simulation/test.hdf5", # None, #
    "duration" : 250, # simulation time
    
    "celltypes" : [],
    
    "CellNumbersInFullModel" : {
       "Npyr" :    9000,
        "Npvbas" :  200,
        "Nolm" :    80,
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
        "Npyr" :    500,
        "Npvbas" :  100,
        "Nolm" :    40,
        "Ncckbas" : 80,
        "Nivy" :    130,
        "Nngf" :    65,
        "Nbis" :    35,
        "Naac" :    30,
        "Nsca" :    20,
        
        
        "Nca3" : 500,
        "Nmec" : 500, 
        "Nlec" : 500,  
        "Nmsteevracells" : 20,
        "Nmskomalicells" : 20,
        "Nmsach"         : 5,
    },
    
    "CellParameters" : {
        "ca3" : {
            "cellclass" : "ArtifitialCell",
            "R" : 0.4,
            "phase" : 1.5,
            "greqs" : 5.0,
            "spike_ train_freq" : 5.0,      
        },
        
        "mec" : {
            "cellclass" : "ArtifitialCell",
            "R" : 0.4,
            "phase" : 0.0,
            "greqs" : 5.0,
            "spike_ train_freq" : 5.0,      
        },
        
        "lec" : {
            "cellclass" : "ArtifitialCell",
            "R" : 0.1,
            "phase" : 0.0,
            "greqs" : 5.0,
            "spike_ train_freq" : 5.0,      
        },
        
        "msteevracells" : {
            "cellclass" : "ArtifitialCell",
            "R" : 0.8,
            "phase" : np.pi,
            "greqs" : 5.0,
            "spike_ train_freq" : 15.0,      
        },
        
        "mskomalicells" : {
            "cellclass" : "ArtifitialCell",
            "R" : 0.8,
            "phase" : 0.0,  # !!!!
            "greqs" : 5.0,
            "spike_ train_freq" : 15.0,      
        },
        
        "msach" : {
            "cellclass" : "ArtifitialCell",
            "R" : 0.4,
            "phase" : np.pi,  # !!!!
            "greqs" : 5.0,
            "spike_ train_freq" : 10.0,      
        },
        
        "pyr" : {
            "cellclass" : "CA1PyramidalCell", # "poolosyncell", # 
            "iext" : 0.007,
            "iext_std" : 0.005,
        },
        
        "pvbas" : {
            "cellclass" : "pvbasketcell",
            "iext" : 0.0,
            "iext_std" : 0.005,
        },
        
        "cckbas" : {
            "cellclass" : "cckcell",
            "iext" : 0.003,
            "iext_std" : 0.005,
        },

        "olm" : {
            "cellclass" : "olmcell",
            "iext" : 0.0,
            "iext_std" : 0.005,
        },
        
        "aac" : {
            "cellclass" : "axoaxoniccell",
            "iext" : 0.0,
            "iext_std" : 0.005,
        },
        
        "ngf" : {
            "cellclass" : "ngfcell",
            "iext" : 0.001,
            "iext_std" : 0.005,
        },
        
        "ivy" : {
            "cellclass" : "ivycell",
            "iext" : 0.003,
            "iext_std" : 0.005,
        },
    
        "bis" : {
            "cellclass" : "CA1BistratifiedCell", # "bistratifiedcell",
            "iext" : 0.002,
            "iext_std" : 0.005,
        },
        
        "sca" : {
            "cellclass" : "scacell",
            "iext" : 0.0,
            "iext_std" : 0.005,
        },
    
    },
    
    "save_soma_v" : {
        "pyr" : [0, ],
        "pvbas" : [0, ],
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
            "gmax": 0.016,
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

            "prob": 0.4,
            
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

            "prob": 0.4,
            
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
            "tau_decay": 44.2,

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
            "tau_rise": 9,
            "tau_decay": 39,

            "prob": 0.29,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "rad_list",
        },
        # end connection to pyramids
        
        # connection to pvbas
        "ca32pvbas": {
            "gmax": 0.7,
            "gmax_std" : 0.2,
            
            "Erev": 0,
            "tau_rise": 2.0,
            "tau_decay": 6.3,

            "prob": 0.02,
            
            "delay": 1.5,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "dendrite_list",
        },
        
        "pyr2pvbas": {
            "gmax": 0.05,
            "gmax_std" : 0.04,
            
            "Erev": 0,
            "tau_rise": 0.07,
            "tau_decay": 0.2,

            "prob": 0.13,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "axon",
            "target_compartment" : "dendrite_list",
        },
        
        "pvbas2pvbas": {
            "gmax": 0.023,
            "gmax_std" : 0.01,
            
            "Erev": -75,
            "tau_rise": 0.8,
            "tau_decay": 4.8,

            "prob": 0.7,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "cckbas2pvbas": {
            "gmax": 1.0,
            "gmax_std" : 0.2,
            
            "Erev": -75,
            "tau_rise": 0.43,
            "tau_decay": 4.49,

            "prob": 0.38,
            
            "delay": 4.5,
            "delay_std" : 2.0,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "olm2pvbas": {
            "gmax": 0.73,
            "gmax_std" : 0.35,
            
            "Erev": -75,
            "tau_rise": 0.25,
            "tau_decay": 7.5,

            "prob": 0.5, # optimized
            
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

            "prob": 0.5, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "ngf2pvbas": {
            "gmax": 0.1,
            "gmax_std" : 0.05,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.5, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "ivy2pvbas": {
            "gmax": 0.1,
            "gmax_std" : 0.05,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.5, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        "sca2pvbas": {
            "gmax": 0.1,
            "gmax_std" : 0.05,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.5, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        
        # end connection to pvbas
        
        # connections to cckbas
        "msteevracells2cckbas" : {
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
            "gmax": 1.0,
            "gmax_std" : 0.2,
            
            "Erev": -75,
            "tau_rise": 0.2,
            "tau_decay": 4.2,

            "prob": 0.63,
            
            "delay": 2.7,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "soma",
        },
        
        # hypotetical connections
        "olm2cckbas": {
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
        
        "bis2cckbas": {
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
        
        "ngf2cckbas": {
            "gmax": 1.5,
            "gmax_std" : 0.7,
            
            "Erev": -75,
            "tau_rise": 0.5,
            "tau_decay": 4.0,

            "prob": 0.5, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "soma",
        },
        
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

            "prob": 0.05,
            
            "delay": 2.5,
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

            "prob": 0.05,
            
            "delay": 2.5,
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

            "prob": 0.5, 
            
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

            "prob": 0.5, 
            
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

            "prob": 0.8, 
            
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

            "prob": 0.5, 
            
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

            "prob": 0.5, 
            
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

            "prob": 0.5, 
            
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
            
            "prob": 0.9,
            
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

            "prob": 0.1, # 0.081,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "axon",
            "target_compartment" : "soma",
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

            "prob": 0.1,
            
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

            "prob": 0.5,
            
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

            "prob": 0.5,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
        # end connections to bis
        
        
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

            "prob": 0.1, 
            
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

            "prob": 0.5, 
            
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

            "prob": 0.1,
            
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

            "prob": 0.06, # ! need to optimize
            
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

            "prob": 0.06, # ! need to optimize
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "dendrite_list",
        },
        
        "olm2ngf": {
            "gmax": 1.27,
            "gmax_std" : 0.6,
            
            "Erev": -75,
            "tau_rise": 1.3,
            "tau_decay": 10.2,

            "prob": 0.1,
            
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

            "prob": 0.5, 
            
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

            "prob": 0.5, 
            
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

            "prob": 0.5, 
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dendrite_list",
        },
             

    }, # end of connetion settings

}


cell_types_in_model = []

for celltype, numbers in sorted(basic_params["CellNumbers"].items()):
    
    celltype = celltype[1:]
    cell_types_in_model.extend( [celltype, ] * numbers )

basic_params["celltypes"] = cell_types_in_model



save_soma_v_idx = np.empty(shape=0, dtype=np.int)
for celltype, list_idx in basic_params["save_soma_v"].items(): 

    indices = [i for i, x in enumerate(basic_params["celltypes"]) if x == celltype]
    if len(indices) == 0:
        continue

    indices = np.asarray(indices)
    list_idx = np.asarray(list_idx)
    
    save_soma_v_idx = np.append(save_soma_v_idx, indices[list_idx])
    
    
basic_params["save_soma_v"]["vect_idxes"] = save_soma_v_idx


for connname, conn_data in basic_params["connections"].items():
    
    conn_data["gmax"] *= 0.001       # recalulate nS to micromhos 
    conn_data["gmax_std"] *= 0.001
    conn_data["delay"] += 1.5        # add delay on spike generation
    
    precell, postcell = connname.split("2")
    
    conn_data["prob"] *= basic_params["CellNumbersInFullModel"]["N"+precell] / basic_params["CellNumbers"]["N"+precell]


# print(basic_params["connections"]["ca32pyr"])




