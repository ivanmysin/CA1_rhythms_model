import numpy as np
import matplotlib.pyplot as plt
from scipy.special import i0 as bessel



def r2kappa(R):
    if R < 0.53:
        kappa = 2 * R + R**3 + 5/6 * R**5

    elif R >= 0.53 and R < 0.85:
        kappa = -0.4 + 1.39 * R + 0.43 / (1 - R)

    elif R >= 0.85:
        kappa = 1 / (3*R - 4*R**2 + R**3)


    I0 = bessel(kappa)

    return kappa, I0
