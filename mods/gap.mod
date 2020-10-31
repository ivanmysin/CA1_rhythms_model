NEURON {
	POINT_PROCESS GAP
	NONSPECIFIC_CURRENT i
	RANGE r, i, vgap
	: POINTER vgap
}

PARAMETER {
	v (millivolt)
	vgap (millivolt)
	r = 100000(megohm)
}

ASSIGNED {
	i (nanoamp)
}

BREAKPOINT {
	i = (v - vgap) / r
}
