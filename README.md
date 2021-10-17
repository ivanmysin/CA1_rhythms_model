Code of a CA1 field model
=========================

This is a large-scale biologically plausible network model of rhythms in the hippocampal CA1 field.

Dependencies
-----------------------------------
Model is runned under Python 3.7. OS is Ubuntu 18.04 or Ubuntu 20.04, another os in not tested.

We will need to install git, pip, and mpich for MPI support:

    sudo apt update
    sudo apt install git python3-pip mpich


Python packages for simulations:
* NEURON 7.6+
* LFPsimpy with our modifications <https://github.com/ivanmysin/LFPsimpy>
* mpi4py

Packages for saving, processing and plotting:
* numpy, scipy, matplotlib
* h5py
* elephant

Installation pakages via pip:
      
    sudo pip3 install numpy scipy matplotlib neuron mpi4py h5py elephant

Directories and files
-----------------------------------
     /cells - directory with models of cells (hoc files)
     /mod - directory with mechanisms for cells (mod files)
     /Results - directory for saving simulation results and plots
     base_model.py - main python file
     basic_parameters.py - python file containing all parameters of simulation
     nontheta_state_params.py - parameters for non-theta state
     presimulation_lib.py - helper functions for calculating some simulation parameters
     simulation_parallel.py - contains function *run_simulation*, it builds and runs the simulation.
     process.py - process hdf5 file
     processingLib.py - library of funtions, which are used for signals porcessing
     plot_result.py - library of funtions, which are used for plotting
     figure_n.py - files, which are plot figures for article. n is number of figure in article
     

How to run
-----------------------------------
You need:
* Clone this repository and repository with LFPsimpy <https://github.com/ivanmysin/LFPsimpy> to same directory.
Open terminal in working directory and execute comants:

      git clone https://github.com/ivanmysin/CA1_rhythms_model
      git clone https://github.com/ivanmysin/LFPsimpy

* Compile *.mod* files in *./mods* directory with *nrnivmodl* 

      cd ./CA1_rhythms_model/mods 
      nrnivmodl
      cd ../

* Run in terminal:
  
        mpiexec -n nthreads python3 base_model.py
  
where *nthreads* is numbers of CPU cores used for simulation
Simulation results are saved to hdf5 file.
*python3* is the default command for calling the python 3 interpreter, however, it may be different on your system.
Substitute the call of the interpreter for which you have installed dependencies.

* To process the results, run *process.py*.  It will process and save
in the same file, wavelet spectra, bands, distribution of neurons by rhythm phases, etc.
  
      python3 process.py

* Run one of the *figure_2(4, 5, 7, 8).py* file to plot figure. For example:

      python3 figure_2.py

Full simulation need 70 Gb RAM!
Full simulation: 9000 pyramidal cell and CA3 gererators, 200 PV basket cells etc.
You can change cells numbers in *basic_parameters.py* file to reduce RAM usage and computational resources. 

Structure of HDF5 file with results
-----------------------------------
You can use any free convenient program for viewing hdf5 files,
for example, HDF COMPASS or hdfview.

Path for reading datasets from hdf5 file:

simulation time: /time

spike train: /extracellular/electrode_1/firing/origin_data/*neuron_type*/*neuron_number*

*neuron_type* is type of neurons, for example, pyr, aac, pvbas

*neuron_number* is number of neuron in simulation, for example, "neuron_1"

lfp: /extracellular/electrode_1/lfp/origin_data/*channel_number*

*channel_number* is number of channel, for example, "channel_1", 1 is stratum oriens, 10 is stratum lacunosum-moleculare

somatic potential: /intracellular/origin_data/*neuron_number*

*neuron_number* is the same as for spike train, type of neuron has been noted in attributes.
