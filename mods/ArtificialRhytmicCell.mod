


NEURON  { 
  ARTIFICIAL_CELL ArtificialRhytmicCell
  RANGE freqs, latency, maxProb, minProb, phase0, myseed
}

UNITS {
  PI = (pi) (1) 
}


PARAMETER {
    freqs = 5 (Hz)    : frequency of oscillator in Hz
    latency = 10 (ms) : latency of spike generation
    phase0 = 0        : initial phase of oscillator
    minProb = 0.2  <0, 1>   : probability of spike generation in the minima of the oscillator 
    maxProb = 0.8  <0, 1>   : probability of spike generation in the maxima of the oscillator
    myseed = 0
    
   
}

ASSIGNED {
    oscillator
    randflag
    freqs_mega_hz
    oscillator_normolizer
    time_after_spike (ms)
    dt (ms)
 
}


INITIAL {
    
    freqs_mega_hz = freqs * 0.001 : freqs need recalculate to megaHz because t in ms
    oscillator_normolizer = 0.5 * (maxProb - minProb)
    
    time_after_spike = latency + 1
    net_send(1, 2)
    set_seed(myseed)
}


NET_RECEIVE (w) {
    :generate randomflag between 0 and 1
    randflag = scop_random() 
    oscillator = oscillator_normolizer * (cos(2 * PI * freqs_mega_hz * t + phase0) + 1) + minProb

    if (randflag < oscillator && time_after_spike > latency) { : generate spike
        net_send(1, 1)
        net_event(t)
        time_after_spike = 0
    } else {
        time_after_spike = time_after_spike + dt
        net_send(1, 1)
    }
    
    

}
