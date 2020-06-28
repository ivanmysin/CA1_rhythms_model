
import os
import neuron

h = neuron.h
h.load_file("stdgui.hoc")
h.load_file("import3d.hoc")
neuron.load_mechanisms("./mods/")
# h.cvode.use_fast_imem(1)




cell_path = "./cells/"
for file in os.listdir(cell_path):
    if file.find(".hoc") != -1:
        h.load_file(cell_path + file)

from simulation import run_simulation
from basic_parameters import basic_params

run_simulation(basic_params, h)
