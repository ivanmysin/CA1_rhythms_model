import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt
import h5py
from scipy.stats import linregress
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
        slopes = np.linspace(-100, 100, 1000000)
        D = []

        for slope in slopes:
            d = self.get_circ_linear_distance(slope)
            D.append(d)

        slope0 = slopes[np.argmin(np.asarray(D))]

        optim_results = minimize(self.get_circ_linear_distance, slope0, method="COBYLA")

        self.slope = optim_results.x
        self.phi_0 = self.angle_shift_from_slope(self.slope)

        return self.slope, self.phi_0

    def transpose(self, x):
        phi_target = 2 * np.pi * self.slope * x + self.phi_0
        return phi_target


def angles2range(phis):
    phis = phis % (2 * np.pi)
    phis[phis > np.pi] = phis[phis > np.pi] - 2 * np.pi
    phis[phis < -np.pi] = phis[phis < -np.pi] + 2 * np.pi
    return phis


def get_place_phase(filepath):
    x_4_preccs = np.empty(0, dtype=np.float)
    y_4_preccs = np.empty(0, dtype=np.float)

    with h5py.File(filepath, 'r') as h5file:
        # sampling_rate = h5file["extracellular/electrode_1/lfp/origin_data"].attrs["SamplingRate"]
        # theta_signal = h5file["extracellular/electrode_1/lfp/processing/bands/channel_1/theta"][:]
        t = h5file["time"][:]
        sampling_rate = 1000 / (t[1] - t[0])

        theta_phases = 2 * np.pi * 0.007 * t  # np.angle( hilbert(theta_signal) ) + np.random.rand() * 2 * np.pi - np.pi #
        theta_phases = theta_phases % (2 * np.pi)
        # theta_phases[theta_phases>np.pi] -= 2*np.pi
        theta_signal = np.cos(theta_phases)

        # plt.plot(t, theta_phases)

        Npyr = 80
        pyr_coord_x = np.zeros(Npyr) + 1000  # np.cumsum( np.zeros(Npyr) + 3 ) + 1000 #
        # pyr_coord_x[pyr_coord_x.size//2:] = np.nan

        firing_group = h5file["extracellular/electrode_1/firing/origin_data/pyr"]  # pyr !!!!
        # sampling_rate *= 0.001

        # ax_out.set_title("Out")

        # for neuron_idx, firing in enumerate(firing_group.values()):

        for neuron_idx, (cell_key, firing) in enumerate(sorted(firing_group.items(), key=lambda x: int(x[0].split("_")[-1]), )):
            if firing.size < 4: continue

            firing = firing[:] * 0.001

            #firing = np.linspace(0, 2, 2000)

            indexes = (np.floor(firing * sampling_rate) - 1).astype(np.int)

            place_center = pyr_coord_x[neuron_idx] * 0.001  # np.median(firing) #
            if np.isnan(place_center) or place_center < 0.3 or place_center > 2:
                continue

            # print(place_center)

            place_center = place_center - 0.2

            firing_during_place = firing - place_center

            # if np.std(firing_during_place) > 5000: continue

            is_inside = np.abs(firing_during_place) < 2

            phases_during_place = theta_phases[indexes]

            firing_inside = firing_during_place[is_inside]
            phases_inside = phases_during_place[is_inside]

            # ax_in.scatter(firing_inside, phases_inside, s=2)
            # ax_in.scatter(firing_inside, phases_inside+2*np.pi, s=2)

            x_4_preccs = np.append(x_4_preccs, firing_inside)
            y_4_preccs = np.append(y_4_preccs, phases_inside)
            # is_outside = np.logical_not(is_inside)
            # firing_outside = firing_during_place[is_outside]
            # phases_outside = phases_during_place[is_outside]

            # ax_out.scatter(firing_outside, phases_outside, s=2)
            # print(neuron_idx)
            break
    return x_4_preccs, y_4_preccs


path = "../../../Data/CA1_simulation/"
files = ["chan_1", ]  # ["test", "test2", "test3"]

x_4_preccs = np.empty(0, dtype=np.float)
y_4_preccs = np.empty(0, dtype=np.float)

for file in files:
    filepath = path + file + ".hdf5"  # "../../Data/CA1_simulation/test3.hdf5"
    print(filepath)

    x_4_preccs_tmp, y_4_preccs_tmp = get_place_phase(filepath)

    x_4_preccs = np.append(x_4_preccs, x_4_preccs_tmp)
    y_4_preccs = np.append(y_4_preccs, y_4_preccs_tmp)

y_4_preccs[y_4_preccs < 0] = y_4_preccs[y_4_preccs < 0] + 2 * np.pi
# phases = np.linspace(0, 2*np.pi, 50)
# cos_line = 200*np.cos(phases) + 800
fig_in, ax_in = plt.subplots(figsize=(5, 5))
# fig_out, ax_out = plt.subplots()


ax_in.set_title("In")
ax_in.scatter(x_4_preccs, y_4_preccs, s=2)

# line_x = np.array([-1.0, 1.0])
# line_y = line_x * res.slope + res.intercept
# regressor = CircularLinearRegession(y_4_preccs, x_4_preccs)
# slope, phi_0 = regressor.fit()

# print(slope, phi_0)
# res = linregress(x_4_preccs, y=y_4_preccs)
# line_y = regressor.transpose(x_4_preccs)

# line_y = angles2range(line_y)
# line_y[line_y < 0] += 2*np.pi

# ax_in.scatter(x_4_preccs, line_y, color="red") #, linewidth=3)
# ax_in.plot(cos_line, phases, color="black", linewidth=1)

# print(res.rvalue**2, res.pvalue)
# ax_in.set_xlim(-2, 2)
ax_in.set_ylim(0, 2*np.pi)
plt.show()