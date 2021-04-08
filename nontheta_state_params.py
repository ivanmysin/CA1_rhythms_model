import numpy as np


# from basic_parameters_nice import get_basic_params
#basic_params = get_basic_params()

def theta_state2non_theta_state_params(basic_params):


    Npyr = 6000
    Nca3_spatial = 20 # 50 # 1200
    Npvbas = basic_params["CellNumbers"]["Npvbas"]


    basic_params["CellNumbers"]["Nmec"] = 0 # remove mec input
    basic_params["CellNumbers"]["Nlec"] = 0 # remove lec input
    basic_params["CellNumbers"]["Nmsteevracells"] = 0 # remove ms teevra cells input
    basic_params["CellNumbers"]["Nmskomalicells"] = 0 # remove ms komali cells input
    basic_params["CellNumbers"]["Nmsach"] = 0 # remove ms cholinergic input
    basic_params["CellNumbers"]["Nca3_non_spatial"] = 0 # remove ca3 non spatial input
    basic_params["CellNumbers"]["Nca3_spatial"] = Nca3_spatial # modify ca3 spatial input

    basic_params["CellNumbers"]["Ncckbas"] = 0 # remove cck basket neurons
    basic_params["CellNumbers"]["Naac"] = 0   # remove  aac neurons
    basic_params["CellNumbers"]["Npyr"] = Npyr
    basic_params["CellNumbers"]["Npvbas"] = Npvbas

    basic_params["duration"] = 800
    basic_params["del_start_time"] = 200


    basic_params["CellParameters"]["ca3_spatial"]["Rtheta"] = 0.3 # coupling to slow gamma
    basic_params["CellParameters"]["ca3_spatial"]["low_mu"] = 0   #
    basic_params["CellParameters"]["ca3_spatial"]["low_freqs"] = 35.0
    basic_params["CellParameters"]["ca3_spatial"]["Rgamma"] = 0.4 # coupling to ripple oscillation
    basic_params["CellParameters"]["ca3_spatial"]["high_mu"] = 0.8 # np.pi
    basic_params["CellParameters"]["ca3_spatial"]["high_freqs"] = 170.0
    basic_params["CellParameters"]["ca3_spatial"]["place_t_radius"] = 2
    basic_params["CellParameters"]["ca3_spatial"]["latency"] = 2


    basic_params["pyr_coodinates"] = np.cumsum( np.zeros(Npyr) + 0.075) + 200
    basic_params["ca3_coodinates"] = np.sort(np.random.normal(loc=350, scale=30.0, size=Nca3_spatial))
    
    
           # np.cumsum( np.zeros(Nca3_spatial) + 0.075) + 300
    basic_params["pvbas_coodinates"]  = np.cumsum( np.zeros(Npvbas) + 3.75)
    basic_params["var_conns_on_pyr"] = basic_params["var_conns_on_pyr"] / 16000 

    basic_params["file_results"] = basic_params["file_results"].split(".hdf5")[0] + "_ripples.hdf5"
    
    return basic_params










