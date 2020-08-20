from neuron import h, load_mechanisms
import os
pc = h.ParallelContext()

#Model
# cell = h.IntFire1()
# cell.refrac = 0 # no limit on spike rate
h.load_file("stdgui.hoc")
h.load_file("stdrun.hoc")
h.load_file("import3d.hoc")
load_mechanisms("../mods/")


for cellfile in os.listdir("../cells/"):
    _, ext = os.path.splitext(cellfile)
    if ext != ".hoc": continue
    h.load_file("../cells/" + cellfile)


cell = h.pvbasketcell(0, 0)




pc.set_gid2node(pc.id(), pc.id())
firing = h.NetCon(cell.soma[0](0.5)._ref_v, None, sec=cell.soma[0])
pc.cell(0, firing) # generates a spike with gid=0
nclist = [pc.gid_connect(i, cell.soma[0]) for i in range(4)] #note gid=0 recursive connection


for i, nc in enumerate(nclist):
  nc.weight[0] = 2 # anything above 1 causes immediate firing for IntFire1
  nc.delay = 1 + 0.1*i # incoming (t, gid) generates output (t + 1 + 0.1*gid, 0)

# Record all spikes (cell is the only one generating output spikes)
out = [h.Vector() for _ in range(2)]
pc.spike_record(-1, out[0], out[1])

#PatternStim
tvec =   h.Vector(range(10))
gidvec = h.Vector(range(10)) # only 0,1,2 go to cell
ps = h.PatternStim()
ps.play(tvec, gidvec)

#Run
pc.set_maxstep(10.)
h.finitialize()
pc.psolve(7)

for i, tsp in enumerate(out[0]):
  print ("%g %d" %(tsp, int(out[1][i])))
