TITLE Ohmic external noisy Current
:
: Ohmic external noisy current that can be set on a per-section basis
:
UNITS {
    (mcA) = (microamp)
    (mV) = (millivolt)
    (nA) = (nanoamp)
    (S) = (siemens)
    (mS) = (millisiemens)
}

: INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
    SUFFIX IextNoise
    NONSPECIFIC_CURRENT iext
    RANGE mean, sigma, tau, myseed
}

PARAMETER {
    mean = 0 (mcA / cm2)
    sigma = 0.001 (mcA / cm2 )
    tau = 15 (ms)
    myseed = 1
    dt (ms)
}

ASSIGNED {
    iext  (mcA/cm2)
    : dt (ms)
}

INITIAL {
    iext = 0
    set_seed(myseed)
}

BREAKPOINT {
    SOLVE noise
}

PROCEDURE noise() {
    : printf("%f", dt )
    iext = - mean + sigma * normrand(0, 1) * sqrt(1/dt)   


}

