import numpy as np
import matplotlib.pyplot as plt
from scipy.special import i0 as bessel



def r2kappa(R):
    if R < 0.53:
        kappa = 2 * Rsetted + Rsetted**3 + 5/6 * Rsetted**5

    elif Rsetted >= 0.53 and Rsetted < 0.85:
        kappa = -0.4 + 1.39 * Rsetted + 0.43 / (1 - Rsetted)

    elif Rsetted >= 0.85:
        kappa = 1 / (3*Rsetted - 4*Rsetted**2 + Rsetted**3)


    I0 = bessel(kappa)

    return kappa, I0
