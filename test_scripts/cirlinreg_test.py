import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize


class CircularLinearRegession:
    def __init__(self, phis, x):
        self.phis = phis
        self.x = x

    def angle_shift_from_slope(self, slope):
        phi_0 = np.angle(np.sum(np.exp(1j * (self.phis - 2 * np.pi * slope * self.x))))
        return phi_0

    def get_circ_linear_distance(self, slope):
        phi_0 = self.angle_shift_from_slope(slope)

        D = 2 * (1 - np.mean(np.cos(self.phis - 2 * np.pi * slope * self.x - phi_0)))

        return D

    def fit(self):
        slopes = np.linspace(-10, 10, 1000)
        D = []

        for slope in slopes:
            d = self.get_circ_linear_distance(slope)
            D.append(d)

        slope0 = slopes[ np.argmin(np.asarray(D)) ]
        optim_results = minimize(self.get_circ_linear_distance, slope0, method="BFGS")

        self.slope = optim_results.x
        self.phi_0 = self.angle_shift_from_slope(self.slope)

        return self.slope, self.phi_0

    def transpose(self, x):
        phi_target = 2 * np.pi * self.slope * x + self.phi_0
        return phi_target


def angles2range(phis):
    phis = phis % (2 * np.pi)
    phis[phis > np.pi] = phis[phis > np.pi] - 2*np.pi
    phis[phis < -np.pi] = phis[phis < -np.pi] + 2*np.pi
    return phis

x = np.linspace(-1, 1, 100)
phis = 2 * np.pi * 0.5 * x + 1.5 + np.random.vonmises(0, 0.5, size=x.size)
phis = angles2range(phis)
reg = CircularLinearRegession(phis, x)



# print( reg.angle_shift_from_slope(-1.5) )

a, ph0 = reg.fit()

pht = reg.transpose(x)
print(a, ph0)
pht = angles2range(pht)

plt.scatter(x, phis, color="blue", s=10)
plt.scatter(x, pht, color="red", s=5)

plt.show()

