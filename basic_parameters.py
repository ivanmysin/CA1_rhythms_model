
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
    "Nelecs" : 10,      # number of electrodes
    "PyrDencity" : 0.2, # pyramidal cells / micrometer^2
    
    "file_results":  "/home/ivan/Data/CA1_simulation/test.hdf5", # None, #
    
    "Npyr" : 1,
    "Npvbas" : 1,
    "Nolm" : 0,
    "Ncckbas" : 0,
    "Nivy" : 0,
    "Nngf" : 0,
    "Nbis" : 0,
    "Naac" : 0,
    "Nsca" : 0,
    
    
    "Nca3" : 2,
    "Nmec" : 0,
    "Nlec" : 0,
    "Nmsteevracells" : 0,
    "Nmskomalicells" : 0,
    
    
    "save_soma_" : None,

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
        "gmax": 0.005,
        "gmax_std" : 0.0001,
        
        "sourse_compartment" : "acell",
        "target_compartment" : "dend",
    },



}



"""
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
"""
