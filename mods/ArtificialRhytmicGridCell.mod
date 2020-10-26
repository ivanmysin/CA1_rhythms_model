


NEURON  { 
  ARTIFICIAL_CELL ArtificialRhytmicGridCell
  RANGE low_freqs, low_mu, low_kappa, low_I0
  RANGE high_freqs, high_mu, high_kappa, high_I0
  RANGE myseed, delta_t, spike_rate, latency
  RANGE grid_freqs, grid_kappa, grid_I0, grid_phase
}

UNITS {
  PI = (pi) (1) 
}


PARAMETER {
    low_freqs = 5 (Hz)     : frequency of oscillator in Hz
    high_freqs = 35 (Hz)   : frequency of oscillator in Hz
    
    latency = 10 (ms)      : latency of spike generation
    spike_rate = 5         : spike rate in spikes per second
    
    low_kappa = 0.4        : kappa of von Mises distribution
    low_I0 = 1.04          : zero order Bessel function 
    low_mu = 0             : mean phase of von Mises distribution
    
    high_kappa = 0.4       : kappa of von Mises distribution
    high_I0 = 1.04         : zero order Bessel function 
    high_mu = 0            : mean phase of von Mises distribution
    
    grid_freqs = 0.1 (Hz)  : frequency of grid cell
    grid_kappa = 0.4       : kappa of grid field for radius of field
    grid_I0 = 1.04         : I0 for radius of field
    grid_phase = 0         : radius of place field
    
    delta_t = 1 (ms)
    myseed = 0
    
   
}

ASSIGNED {
    randflag
    time_after_spike (ms)
    dt (ms)
    low_phase
    high_phase
    grid_current_phase
    
    TWOPI
    LOW_TWOPIIODFIRATIO
    HIGH_TWOPIIODFIRATIO
    GRID_TWOPIIODFIRATIO
    
    
    pdf
    low_pdf
    high_pdf
    grid_pdf
    
    low_delta_phase
    high_delta_phase
    grid_delta_phase
    freqs_ratio
    
    
}


INITIAL {
    set_seed(myseed)
    TWOPI = 2 * PI
    
    low_phase = 0
    high_phase = 0
    grid_current_phase = 0
    pdf = 0
    
    low_delta_phase = low_freqs * TWOPI * 0.001 * delta_t     : rad
    high_delta_phase = high_freqs * TWOPI * 0.001 * delta_t   : rad
    grid_delta_phase = grid_freqs * TWOPI * 0.001 * delta_t   : rad
    
    
    : printf("f: %g ", freqs)
    : freqs_ratio = spike_rate / low_freqs                  : spikes per cycle of oscillation

    LOW_TWOPIIODFIRATIO = low_delta_phase  / (TWOPI * low_I0)
    HIGH_TWOPIIODFIRATIO = high_delta_phase  / (TWOPI * high_I0)
    GRID_TWOPIIODFIRATIO = grid_delta_phase  / (TWOPI * high_I0)
    
    time_after_spike = latency + 1

    
    get_pdf_by_phase()
    net_send(1, 2)
    
}

NET_RECEIVE (w) {
   
    get_pdf_by_phase()
         
    low_phase = low_phase + low_delta_phase
    high_phase = high_phase + high_delta_phase
    grid_current_phase = grid_current_phase + grid_delta_phase


    randflag = scop_random() : generate randomflag between 0 and 1
        
    if (randflag < pdf  && time_after_spike > latency) {
        : generate spike
        time_after_spike = 0
        net_send(delta_t, 1)
        net_event(t)
       
    } else {
        time_after_spike = time_after_spike + delta_t
        net_send(delta_t, 1)
    }
    

}


PROCEDURE get_pdf_by_phase() {
    
    : TABLE pdf DEPEND phase FROM -4 TO 4 WITH 100
    
    low_pdf = exp(low_kappa * cos(low_phase - low_mu) ) * LOW_TWOPIIODFIRATIO
    high_pdf = exp(high_kappa * cos(high_phase - high_mu) ) * HIGH_TWOPIIODFIRATIO
    grid_pdf = exp(grid_kappa * cos(grid_current_phase - grid_phase) ) * GRID_TWOPIIODFIRATIO
    
    
    pdf = spike_rate * high_pdf * low_pdf * grid_pdf 
    

}

