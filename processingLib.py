# -*- coding: utf-8 -*-
"""
library for data proceccing
@author: ivan
"""
import numpy as np
import scipy.stats as stat
import scipy.signal as sig
from scipy.ndimage.filters import convolve1d
from scipy.signal.windows import parzen
from elephant import signal_processing as sigp


#####################################################################
def circular_distribution(amples, angles, angle_step, nkernel=15, density=True):
    """
    return circular distribution smoothed by the parsen kernel
    """
    kernel = parzen(nkernel)
    bins = np.arange(-np.pi, np.pi + angle_step, angle_step)
    distr, _ = np.histogram(angles, bins=bins, weights=amples, density=density)

    distr = convolve1d(distr, kernel, mode="wrap")
    bins = np.convolve(bins, [0.5, 0.5], mode="valid")

    return bins, distr

###############################################################

def get_angles_in_range(angles):
    """
    return angles from -pi to pi
    """
    two_pi = 2 * np.pi
    anles_in_range = angles % (two_pi)
    anles_in_range[anles_in_range < -np.pi] += two_pi
    anles_in_range[anles_in_range >= np.pi] -= two_pi

    return anles_in_range
################################################################

def cossfrequency_phase_amp_coupling(phase_signal, coefAmp, phasebins=20, nkernel=15):
    """
    compute disribution amplitudes by phases of phase_signal
    """
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
    """
    compute n:m test
    """

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
    """
    run cossfrequency_phase_phase_coupling for diffrent bands
    """

    couplings = []
    distrss = []
    for band in bands4highfr:
        high_signal_band = sigp.butter(high_fr_signal, highpass_freq=band[0], lowpass_freq=band[1], order=butter_order, fs=fd )

        coupling, bins, distrs = cossfrequency_phase_phase_coupling(low_fr_signal, high_signal_band, nmarray, thresh_std=thresh_std, circ_distr=circ_distr)

        couplings.append(coupling)
        distrss.append(distrs)

    return couplings, bins, distrss
###################################################################
def get_phase_disrtibution(train, lfp, fs):
    """
    compute disrtibution of spikes by phases of LFP
    """
    if train.size == 0:
        return np.empty(0, dtype=np.float), np.empty(0, dtype=np.float)

    nkernel = 15

    analitic_signal = sig.hilbert(lfp)
    lfp_phases = np.angle(analitic_signal, deg=False)
    lfp_ampls = np.abs(analitic_signal)

    train = np.floor(train * fs * 0.001).astype(np.int) # multiply on 0.001 because train in ms, fs in Hz

    train = train[train < lfp.size-1]

    train_phases = lfp_phases[train]
    train_ampls = lfp_ampls[train]

    R = np.abs( np.mean(analitic_signal[train]) )

    count, bins = np.histogram(train_phases, bins=50, density=True, range=[-np.pi, np.pi], weights=train_ampls )

    kernel = parzen(nkernel)

    # distr, _ = np.histogram(angles, bins=bins, weights=amples, density=density)

    count = convolve1d(count, kernel, mode="wrap")

    bins = np.convolve(bins, [0.5, 0.5], mode="valid")
    return bins, count, R

#################################################################

def current_sourse_density(lfp, dz=1):
    """
    compute CSD
    """
    lfp = np.asarray(lfp)
    weights = np.array([1, -2, 1]) / dz**2
    csd = convolve1d(lfp, weights, axis=0, mode="nearest")
    return csd
    
#################################################################

def get_modulation_index(W4phase, W4ampls, nbins=20):
    """
    compule modulation index
    """

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
########################################################################

def slice_by_bound_values(arr, left_bound, right_bound):
    sl = np.s_[ np.argmin(np.abs(arr-left_bound)) : np.argmin(np.abs(arr-right_bound)) ]
    
    return sl








