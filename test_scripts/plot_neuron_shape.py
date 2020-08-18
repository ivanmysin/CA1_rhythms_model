import os
os.chdir("../")
from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import neuron
from neuron import h
h.load_file("stdgui.hoc")
h.load_file("import3d.hoc")
neuron.load_mechanisms("./mods/")

os.chdir("./cells/")
# h.load_file("class_cckcell.hoc")
# h.load_file("class_ivycell.hoc")
# h.load_file("class_axoaxoniccell.hoc")
# h.load_file("class_bistratifiedcell.hoc")
# h.load_file("class_cutsuridiscell.hoc")
# h.load_file("class_ngfcell.hoc")
# h.load_file("class_olmcell.hoc")
# h.load_file("class_poolosyncell.hoc")
# h.load_file("class_pvbasketcell.hoc")
# h.load_file("class_scacell.hoc")
h.load_file("CA1PC.hoc")
# cell = h.bistratifiedcell(0, 0)
# h.axoaxoniccell(0, 0)
# h.ivycell(0, 0)
# h.cckcell(0, 0)
# cell = h.cutsuridiscell(0, 0) 
# cell = h.ngfcell(0, 0) 
# cell = h.olmcell(0, 0) 
# cell = h.poolosyncell()

cell1 = h.CA1PyramidalCell(0, 0)
cell1.position(-200, 0, 0)

cell2 = h.CA1PyramidalCell(0, 0)
cell2.position(200, 0, 0)
# cell2 = h.poolosyncell() 
# cell2.position(200, 0, 0)
# cell = h.pvbasketcell() 
# cell = h.scacell(0, 0)

#cell3 = h.poolosyncell()
# cell3.position(0, 0, -200)

el_x = np.zeros(10)
el_y = np.linspace(-300, 800, 10)
el_z = np.zeros(10)


# h.load_file('c91662.ses')
# sl = h.SectionList([sec for sec in h.allsec() if 'apic' in str(sec)])
# for sec in sl:
    # sec.v = 0

fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')


ps = h.PlotShape(False) # cell.all, 
ps.scale(-80, 40)
ps.variable('v')
ax_ps = ps.plot(fig, cmap=cm.jet) #  


# print(len(fig.axes))
fig.axes[0].scatter(el_x, el_y, el_z, color="red", s = 10)
fig.axes[0].view_init(-90, 90)
plt.show()
