# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 14:10:11 2014
library for data proceccing 
@author: ivan
"""
import numpy as np
import scipy.stats as stat
import scipy.signal as sig
from scipy.ndimage.filters import convolve1d
from scipy.signal.windows import parzen
from elephant import signal_processing as sigp
from elephant.current_source_density import estimate_csd

#####################################################################
def circular_distribution(amples, angles, angle_step, nkernel=15, density=True):

    kernel = parzen(nkernel)
    bins = np.arange(-np.pi, np.pi + angle_step, angle_step)
    distr, _ = np.histogram(angles, bins=bins, weights=amples, density=density)

    distr = convolve1d(distr, kernel, mode="wrap")
    bins = np.convolve(bins, [0.5, 0.5], mode="valid")

    return bins, distr

###############################################################

def get_angles_in_range(angles):
    two_pi = 2 * np.pi
    anles_in_range = angles % (two_pi)
    anles_in_range[anles_in_range < -np.pi] += two_pi
    anles_in_range[anles_in_range >= np.pi] -= two_pi

    return anles_in_range
################################################################

def cossfrequency_phase_amp_coupling(phase_signal, coefAmp, phasebins=20, nkernel=15):
    phase_signal = np.angle(sig.hilbert(phase_signal), deg=False)

    coefAmp = np.abs(coefAmp)
    coefAmp = stat.zscore(coefAmp, axis=1)

    coupling = np.empty(shape=(coefAmp.shape[0], phasebins), dtype=np.float)

    kernel = parzen(nkernel)
    for freq_idx in range(coefAmp.shape[0]):
        coup, _ = np.histogram(phase_signal, bins=phasebins, weights=coefAmp[freq_idx, :], range=[-np.pi, np.pi])
        coup = convolve1d(coup, kernel, mode="wrap")
        coupling[freq_idx, :] = coup
    coupling = coupling /(coupling.max() - coupling.min())
    return coupling

###################################################################
def cossfrequency_phase_phase_coupling(low_fr_signal, high_fr_signal, nmarray, thresh_std=None, circ_distr=False):
    coupling = np.zeros(nmarray.size)

    low_fr_analitic_signal = sig.hilbert(low_fr_signal)
    high_fr_analitic_signal = sig.hilbert(high_fr_signal)

    if not thresh_std is None:

        abs_signal = np.abs(low_fr_analitic_signal * high_fr_analitic_signal)

        signif_poits = abs_signal > (np.mean(abs_signal) + thresh_std * np.std(abs_signal))

        low_fr_analitic_signal = low_fr_analitic_signal[signif_poits]
        high_fr_analitic_signal = high_fr_analitic_signal[signif_poits]

        if low_fr_analitic_signal.size == 0:
            return coupling

    low_fr_angles = np.angle(low_fr_analitic_signal, deg=False)
    high_fr_angles = np.angle(high_fr_analitic_signal, deg=False)

    distrs = []
    bins = []
    for i in range(nmarray.size):

        vects_angle = low_fr_angles * nmarray[i] - high_fr_angles
        x_vect = np.cos(vects_angle)
        y_vect = np.sin(vects_angle)
        mean_resultant_length = np.sqrt(np.sum(x_vect)**2 + np.sum(y_vect)**2) / vects_angle.size
        coupling[i] = mean_resultant_length

        if circ_distr:
            vects_angle = get_angles_in_range(vects_angle)
            bins_anles, distr = circular_distribution(np.ones_like(vects_angle), vects_angle, angle_step=0.1,
                                                      nkernel=15)

            distrs.append(distr)
            bins.append(bins_anles)

    return coupling, bins, distrs
###################################################################
def phase_phase_coupling(low_fr_signal, high_fr_signal, bands4highfr, fd, nmarray, thresh_std=None, circ_distr=False, butter_order=2):
    import matplotlib.pyplot as plt
    couplings = []
    distrss = []
    for band in bands4highfr:
        high_signal_band = sigp.butter(high_fr_signal, highpass_freq=band[0], lowpass_freq=band[1], order=butter_order, fs=fd )

        coupling, bins, distrs = cossfrequency_phase_phase_coupling(low_fr_signal, high_signal_band, nmarray, thresh_std=thresh_std, circ_distr=circ_distr)

        couplings.append(coupling)
        distrss.append(distrs)

    return couplings, bins, distrss
###################################################################
def get_asymetry_index(lfp, orders = 25):
    idx_max = sig.argrelmax(lfp, order=orders)[0]
    idx_min = sig.argrelmax(-lfp, order=orders)[0]

    assymetry_index = np.array([], dtype=float)
    n = np.min([idx_max.size, idx_min.size])
    for idx in range(n):
        if (idx == 0 or idx+1 == n):
            continue

        if (idx_max[idx] < idx_min[idx] and idx_max[idx+1] > idx_min[idx]):
            asind = np.log( (idx_max[idx] - idx_min[idx-1]) / (idx_min[idx] - idx_max[idx]) )
            assymetry_index = np.append(assymetry_index, asind)

        if (idx_max[idx] > idx_min[idx] and idx_min[idx+1] > idx_max[idx]):
            asind = np.log( (idx_max[idx] - idx_min[idx]) / (idx_min[idx+1] - idx_max[idx]) )
            assymetry_index = np.append(assymetry_index, asind)
    assymetry_index = assymetry_index[np.logical_not( np.isnan(assymetry_index) ) ]
    return assymetry_index, idx_max, idx_min



# def get_units_phase_coupling(lfp, firing, fd):
#     angles = np.array([])
#     length = np.array([])
#     analitic_signal = sig.hilbert(lfp)
#     amp = np.abs(analitic_signal)
#     amp /= np.linalg.norm(amp)
#     lfp_phases = np.angle(analitic_signal, deg=False )
#
#     """
#     if (firing[1, :].size == 0):
#         return 0, 0
#     """
#     start = np.min(firing[1, :]).astype(int)
#     end = np.max(firing[1, :]).astype(int) + 1
#     for idx in range(start, end):
#         spike_times = firing[0, firing[1, :]  == idx]
#         if (spike_times.size == 0):
#             continue
#         spike_ind = np.floor(spike_times*fd).astype(int)
#         spike_phases = lfp_phases[spike_ind]
#         tmp_x = np.sum( amp[spike_ind] * np.cos(spike_phases) )
#         tmp_y = np.sum( amp[spike_ind] * np.sin(spike_phases) )
#         mean_phase = np.arctan2(tmp_y, tmp_x)
#         length_vect = np.sqrt(tmp_x**2 + tmp_y**2) / spike_phases.size
#         angles = np.append(angles, mean_phase)
#         length = np.append(length, length_vect)
#
#     return angles, length

# def get_units_disrtibution(lfp, fd, firing, firing_slices):
#     analitic_signal = sig.hilbert(lfp)
#     lfp_phases = np.angle(analitic_signal, deg=False )
#     neurons_phases = {}
#     for key, sl in firing_slices.items():
#         fir = firing[:, sl]
#         neurons_phases[key] = np.array([], dtype=float)
#         if (fir.size == 0):
#             continue
#         indexes = (fir[0, :] * fd).astype(int)
#         neurons_phases[key] = lfp_phases[indexes]
#
#     return neurons_phases

def get_phase_disrtibution(train, lfp, fs):
    if train.size == 0:
        return np.empty(0, dtype=np.float), np.empty(0, dtype=np.float), np.empty(0, dtype=np.float)



    analitic_signal = sig.hilbert(lfp)
    lfp_phases = np.angle(analitic_signal, deg=False)
    lfp_ampls = np.abs(analitic_signal)

    # print(train[-1]*0.001, " " , (lfp.size-1)/fs)
    train = np.floor(train * fs * 0.001).astype(np.int) # multiply on 0.001 because train in ms, fs in Hz

    train = train[train < lfp.size-1]

    train_phases = lfp_phases[train]
    train_ampls = lfp_ampls[train]

    R = np.abs( np.mean(analitic_signal[train]) )

    count, bins = np.histogram(train_phases, bins=20, density=True, range=[-np.pi, np.pi], weights=train_ampls )
    bins = np.convolve(bins, [0.5, 0.5], mode="valid")
    return bins, count, R

#################################################################

def current_sourse_density(lfp, dz=1):
    lfp = np.asarray(lfp)
    weights = np.array([1, -2, 1]) / dz**2
    csd = convolve1d(lfp, weights, axis=0, mode="nearest")
    return csd
    
#################################################################

def get_modulation_index(W4phase, W4ampls, nbins=20):
    
    Nampls = W4ampls.shape[0]
    Nphs = W4phase.shape[0]
    
    modulation_index = np.zeros( [Nampls, Nphs], dtype=np.float )
    
    unif = 1.0 / (2*np.pi)
    
    ampls = np.abs(W4ampls)
    phases = np.angle(W4phase)
    for idx4ampl in range(Nampls):
        a = ampls[idx4ampl, :]
        for idx4phase in range(Nphs):
            p = phases[idx4phase, :]
            
            
            distr, _ = np.histogram(p, bins=nbins, weights=a, range=[-np.pi, np.pi], density=True)
            distr += 0.000000001
            mi = np.sum(distr * np.log(distr / unif) )
            # distr = distr / np.sum(distr)
            # mi = -np.mean(distr * np.log(distr) )
            ##########
            # x = a * np.cos(p)
            # y = a * np.sin(p)
            # mi = np.sqrt(np.sum(x)**2 + np.sum(y)**2) / np.sum(a)
            
            modulation_index[idx4ampl, idx4phase ] = mi
    
    return modulation_index

def get_mi_by_coherence(phase_band, ampl_w, fd, ph_fr_range=[4, 12], nperseg=4096):
  
    mi = []

    for fr_idx in range(ampl_w.shape[0]):
        
        amples = np.abs(ampl_w[fr_idx, :])
        
        f, Coh = sig.coherence(phase_band, amples, fs=fd, nperseg=nperseg)
        Coh = Coh[ (f>ph_fr_range[0])&(f<ph_fr_range[1]) ]
        
        mi.append(Coh)
    
    f = f[ (f>ph_fr_range[0])&(f<ph_fr_range[1]) ]
    mi = np.vstack(mi)
    return mi, f
########################################################################

def slice_by_bound_values(arr, left_bound, right_bound):
    sl = np.s_[ np.argmin(np.abs(arr-left_bound)) : np.argmin(np.abs(arr-right_bound)) ]
    
    return sl








