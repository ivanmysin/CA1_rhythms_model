import matplotlib.pyplot as plt
import numpy as np
from neuron import h, load_mechanisms
import os


h.load_file("stdgui.hoc")
h.load_file("stdrun.hoc")
h.load_file("import3d.hoc")
# h.nrn_load_dll("../mods/x86_64/.libs/libnrnmech.so")
load_mechanisms("../mods/")


for cellfile in os.listdir("../cells/"):
    _, ext = os.path.splitext(cellfile)
    if ext != ".hoc": continue
    h.load_file("../cells/" + cellfile)


 
# cell = h.poolosyncell(0, 0) 
# cell = h.pvbasketcell(0, 0) 
# cell = h.scacell(0, 0) 
cell = h.CA1BistratifiedCell(0, 0)

sec_list = getattr( cell, "dend" )

len_sec_list = sum(1 for _ in sec_list)

rand_idx = np.random.randint(0, len_sec_list)


for idx, sec in enumerate(sec_list):
    
    if idx == rand_idx: dend = sec
        
sec.insert("IextNoise")
# rad.object(0).insert("IextNoise")

"""
for sec in rad:
    sec.insert("IextNoise")
    sec.sigma_IextNoise = 0.05
    sec.mean_IextNoise = 0.01
"""            
            
            
##==================== stimulus settings ===========================
stim = h.IClamp(0.5, sec=cell.soma[0])
stim.dur   = 5
stim.delay = 150
stim_current = h.Vector()
stim_current.record(stim._ref_i)

syn = h.epsp(dend(0.9))
syn.tau0  = 0.5
syn.tau1 = 5
syn.onset    = stim.delay + 5
syn_current = h.Vector()
syn_current.record(syn._ref_i)

##==================== recording settings ==========================
t = h.Vector()
t.record(h._ref_t)

soma_v = h.Vector()
soma_v.record(cell.soma[0](0.5)._ref_v)

nexus_v = h.Vector()
nexus_v.record(dend(0.9)._ref_v)


##======================== general settings ===================================
h.v_init = -80
h.tstop = 150
h.celsius = 37



#============================= plotting  function ================================
def plot_result(t, soma_v, nexus_v, stim_current, syn_current, show_from = 4400):
    t = np.array(t)[show_from:]
    soma_v = np.array(soma_v)[show_from:]
    nexus_v = np.array(nexus_v)[show_from:]
    stim_current = np.array(stim_current)[show_from:]
    syn_current = np.array(syn_current)[show_from:]
    f, (ax0, ax1, ax2) = plt.subplots(3,1, figsize  = (6.5,3),gridspec_kw = {'height_ratios':[4, 1,1]})
    ax0.plot(t,soma_v, label = 'soma')
    ax0.plot(t,nexus_v, label = 'apic[36]')
    ax0.set_ylabel('Voltage (mV)')
    ax0.set_ylim(-80,40)
    ax0.spines['right'].set_visible(False)
    ax0.spines['top'].set_visible(False)
    ax0.spines['bottom'].set_visible(False)
    ax0.get_xaxis().set_visible(False)
    ax0.legend(frameon=False)

    ax1.plot(t, np.array(syn_current)*-1, color='red', label='EPSP-like current')
    ax1.set_ylim(-0.02,2)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.get_xaxis().set_visible(False)
    ax1.legend(frameon=False)

    ax2.plot(t, stim_current, color='black', label='step current')
    ax2.set_ylabel('Current (nA)', ha='left', labelpad=15)
    ax2.set_xlabel('Time (ms)')
    ax2.set_ylim(-0.02,2)
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.legend(frameon=False)
    
    plt.show(block = True)

#============================= simulation ================================


syn.imax = 0 # 0.5 
stim.amp = 0 # 1.9
h.run()
plot_result(t, soma_v, nexus_v, stim_current, syn_current)


"""
syn.imax = 0
stim.amp = 1.9
h.run()
plot_result(t, soma_v, nexus_v, stim_current, syn_current)


syn.imax = 0.5
stim.amp = 1.9


h.run()
plot_result(t, soma_v, nexus_v, stim_current, syn_current)
"""


"""
t = np.linspace(0, 1, 1000)
s = np.cos(2 * np.pi * t * 5)

freqs = np.linspace(1, 20, 40)

W = sigp.wavelet_transform(s, freqs, nco=6.0, fs=1000)

W = np.abs(W)

plt.pcolor(t, freqs, W)

plt.show()
"""
