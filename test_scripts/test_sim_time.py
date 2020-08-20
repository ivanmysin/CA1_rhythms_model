import numpy as np
from neuron import h, load_mechanisms

h.load_file("stdgui.hoc")
h.load_file("stdrun.hoc")
h.cvode.use_fast_imem(1)
# h.dt = 0.5


from time import time
import os
import sys
sys.path.append("../")
import presimulation_lib as prelib
from basic_parameters import basic_params
from time import time

###### parameters block ############
dur = 1000
test_cell = "ca3"
#####################################

RNG = np.random.default_rng()



load_mechanisms("../mods/")

for cellfile in os.listdir("../cells/"):
    _, ext = os.path.splitext(cellfile)
    if ext != ".hoc": continue
    h.load_file("../cells/" + cellfile)

postsynaptic_cell = "ca3"

cellclass = getattr(h, basic_params["CellParameters"][postsynaptic_cell]["cellclass"])
cell = h.pvbasketcell(0, 0)


Ncells = 1000 # int( basic_params["CellNumbers"]["N"+test_cell] )
cellclass = getattr(h, basic_params["CellParameters"][test_cell]["cellclass"])
cells = [cell, ]
for idx in range(Ncells):
    # tvec = h.Vector( np.linspace(0, 1000, 200) )
    # gidvec = h.Vector()
    
    cell = h.NetStim() # h.PatternStim(tvec)  # cellclass(0, 0) # 
    # cell.play(tvec, gidvec)

    # cell.acell.delta_t = 100 # h.dt
    cells.append(cell)

h.tstop = dur
timer = time()
h.run()
print("Simulation time ", time() - timer)
