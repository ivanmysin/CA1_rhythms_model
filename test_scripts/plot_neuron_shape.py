import os

from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import neuron
from neuron import h
h.load_file("stdgui.hoc")
h.load_file("import3d.hoc")
neuron.load_mechanisms("../mods/")

for cellfile in os.listdir("../cells/"):
    _, ext = os.path.splitext(cellfile)
    if ext != ".hoc": continue
    h.load_file("../cells/" + cellfile)

# cell = h.pvbasketcell(0, 0)
# cell = h.axoaxoniccell(0, 0)
# cell = h.ivycell(0, 0)
# cell = h.cckcell(0, 0)
# cell = h.ngfcell(0, 0)
# cell = h.olmcell(0, 0)
# cell = h.CA1BistratifiedCell(0, 0)
# cell = h.scacell(0, 0)



cell1 = h.CA1PyramidalCell(1, 1)
cell1.position(-200, 0, 0)

for sec in cell1.all:
    sec.v = -50

# cell2 = h.CA1PyramidalCell(0, 0)
# cell2.position(200, 0, 0)
# cell2 = h.poolosyncell() 
# cell2.position(200, 0, 0)
# cell = h.pvbasketcell() 
# cell = h.scacell(0, 0)

#cell3 = h.poolosyncell()
# cell3.position(0, 0, -200)

el_x = np.zeros(10)
el_y = np.linspace(-200, 600, 10)
el_z = np.zeros(10)


# h.load_file('c91662.ses')
# sl = h.SectionList([sec for sec in h.allsec() if 'apic' in str(sec)])
# for sec in sl:
    # sec.v = 0

fig = plt.figure(figsize=(5, 5))
# ax = fig.add_subplot(111, projection='3d')


ps = h.PlotShape(False) # cell.all, 
ps.scale(-70, -40)
#ps.variable('v')
ax_ps = ps.plot(fig, cmap=cm.Reds) #  cm.jet

# print(len(fig.axes))
fig.axes[0].scatter(el_x, el_y, el_z, color="blue", s = 10)

fig.axes[0].set_xlabel(r"$\mu m$")
fig.axes[0].set_ylabel(r"$\mu m$")
fig.axes[0].set_zlabel(r"$\mu m$")

fig.axes[0].view_init(-70, 90) # -90

fig.axes[0].grid(False)
# fig.axes[0].set_xticks([])
# fig.axes[0].set_yticks([])
# fig.axes[0].set_zticks([])

#

plt.show()
fig.savefig("pyr.png")