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
    
    "CellNumbers" : {
        "Npyr" :    9000,    # 
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
            "target_compartment" : "dend",
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
            "target_compartment" : "dend",
        },
        
       "pyr2bis": {
            "gmax": 0.014,
            "gmax_std" : 0.007,
            
            "Erev": 0,
            "tau_rise": 0.11,
            "tau_decay": 0.25,

            "prob": 0.14,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "axon",
            "target_compartment" : "dend",
        },
        
        
       "pyr2axo": {
            "gmax": 0.04,
            "gmax_std" : 0.02,
            
            "Erev": 0,
            "tau_rise": 0.3,
            "tau_decay": 0.6,

            "prob": 0.07,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "axon",
            "target_compartment" : "dend",
        },
        
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
            "target_compartment" : "dend",
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
        
        
       "axo2pyr": {
            "gmax": 20.5,
            "gmax_std" : 10,
            
            "Erev": -75,
            "tau_rise": 0.28,
            "tau_decay": 8.4,

            "prob": 0.29,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "axon",
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
        
       "ca32axo": {
            "gmax": 0.7,
            "gmax_std" : 0.2,
            
            "Erev": 0,
            "tau_rise": 2,
            "tau_decay": 6.3,

            "prob": 0.06,
            
            "delay": 1.5,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "dend",
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
            "target_compartment" : "dend",
        },
        
       "ca32pvbas": {
            "gmax": 0.7,
            "gmax_std" : 0.2,
            
            "Erev": 0,
            "tau_rise": 2.0,
            "tau_decay": 6.3,

            "prob": 0.9,
            
            "delay": 1.5,
            "delay_std" : 0.5,
            

            "sourse_compartment" : "acell",
            "target_compartment" : "dend",
        },
        
       "cckbas2pvbas": {
            "gmax": 1.0,
            "gmax_std" : 0.2,
            
            "Erev": -75,
            "tau_rise": 0.43,
            "tau_decay": 4.49,

            "prob": 0.38,
            
            "delay": 4.5
            "delay_std" : 2.0,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dend",
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
            "target_compartment" : "dend",
        },
        
       "olm2pvbas": {
            "gmax": 0.73,
            "gmax_std" : 0.35,
            
            "Erev": -75,
            "tau_rise": 0.25,
            "tau_decay": 7.5,

            "prob": 0.1,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dend",
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
            "target_compartment" : "dend",
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
             
       "olm2sca": {
            "gmax": 1.3,
            "gmax_std" 0.6: ,
            
            "Erev": -75,
            "tau_rise": 0.07,
            "tau_decay": 29,

            "prob": 0.1,
            
            "delay": 1.2,
            "delay_std" : 0.2,
            

            "sourse_compartment" : "soma",
            "target_compartment" : "dend",
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
            "target_compartment" : "dend",
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
            "target_compartment" : "dend",
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
            "target_compartment" : "dend",
        },
        
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
            "target_compartment" : "dend",
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
            "target_compartment" : "dend",
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

# print(save_soma_v_idx)



"""

    ######################################
        "ca32pyr": {
            "prob": 1.0,
            "tau_rise": 0.5,
            "tau_decay": 5.0,
            "delay": 1.0,
            "delay_std" : 0.2,
            "Erev": 0.0,
            "gmax": 0.05,
            "gmax_std" : 0.0001,

            "sourse_compartment" : "acell",
            "target_compartment" : "soma",
        },
        
        "ca32pvbas": {
            "prob": 1.0,
            "tau_rise": 0.5,
            "tau_decay": 5.0,
            "delay": 1.0,
            "delay_std" : 0.2,
            "Erev": 0.0,
            "gmax": 0.05,
            "gmax_std" : 0.0001,

            "sourse_compartment" : "acell",
            "target_compartment" : "soma",
        },


"pyr2pvbas" : {
            "prob" : 1.0,
            "tau_rise" : 0.5,
            "tau_decay" : 5.0,
            
            "delay" : 1.0,
            "delay_std" : 0.2,
            
            "Erev" : 0.0,
            "gmax" : 0.05,
            "gmax_std" : 0.0001,
            
            "sourse_compartment" : "axon",
            "target_compartment" : "dend",
            
            
        },
        
        "cckbas2pvbas": {
            "prob": 1.0,
            "tau_rise": 0.5,
            "tau_decay": 5.0,
            "delay": 1.0,
            "delay_std" : 0.2,
            "Erev": 0.0,
            "gmax": 0.005,
            "gmax_std" : 0.0001,
            
            "sourse_compartment" : "acell",
            "target_compartment" : "dend",
        },
        
    "pyr2olm": {
        "prob": 0.5,
        "tau_rise": 0.5,
        "tau_decay": 5.0,
        "delay": 1.0,
        "Erev": 0.0,
        "gmax": 0.01,
        
        "sourse_compartment" : "soma",
        "target_comartment" : "dend",
    },


    "pyr2cckbas": {
        "prob": 0.5,
        "tau_rise": 0.5,
        "tau_decay": 5.0,
        "delay": 1.0,
        "Erev": 0.0,
        "gmax": 0.01,
    },



    
    
    "pvbas2pvbas" : {
    
        "prob" : 0.5,
        "tau_rise" : 0.5,
        "tau_decay" : 5.0,
        "delay" : 1.0,
        "Erev" : -70.0,
        "gmax" : 0.1,
    
    },
    
           " 2 ": {
            "gmax": ,
            "gmax_std" : ,
            
            "Erev": ,
            "tau_rise": ,
            "tau_decay": ,

            "prob": ,
            
            "delay": ,
            "delay_std" : ,
            

            "sourse_compartment" : "",
            "target_compartment" : "",
        },

       " 2 ": {
            "gmax": ,
            "gmax_std" : ,
            
            "Erev": ,
            "tau_rise": ,
            "tau_decay": ,

            "prob": ,
            
            "delay": ,
            "delay_std" : ,
            

            "sourse_compartment" : "",
            "target_compartment" : "",
        },
        
       " 2 ": {
            "gmax": ,
            "gmax_std" : ,
            
            "Erev": ,
            "tau_rise": ,
            "tau_decay": ,

            "prob": ,
            
            "delay": ,
            "delay_std" : ,
            

            "sourse_compartment" : "",
            "target_compartment" : "",
        },   
             
       " 2 ": {
            "gmax": ,
            "gmax_std" : ,
            
            "Erev": ,
            "tau_rise": ,
            "tau_decay": ,

            "prob": ,
            
            "delay": ,
            "delay_std" : ,
            

            "sourse_compartment" : "",
            "target_compartment" : "",
        },
"""
