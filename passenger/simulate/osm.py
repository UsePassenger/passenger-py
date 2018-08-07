import random

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from passenger.simulate.distance import alldistance, haversine


class OSMPoints(object):
    def __init__(self, points, limit=1000, start=None, end=None):
        super(OSMPoints, self).__init__()
        self.limit = limit
        self.points = self.__downsample(points)

        lats, lons, names = zip(*self.points)
        self.names = names

        self.z = np.concatenate([
            np.array(lats).reshape(-1, 1),
            np.array(lons).reshape(-1, 1)], axis=1)

        if start is None:
            start = 0
        elif isinstance(start, tuple):
            start = self.find_closest(self.z, start[0], start[1])

        if end is None:
            end = 0
        elif isinstance(end, tuple):
            end = self.find_closest(self.z, end[0], end[1])

        self.start = start
        self.end = end
        self.path = None

    def find_closest(self, z, ax, ay):
        anchor = np.array([ax, ay])
        zplus = np.concatenate([anchor.reshape(1, 2), z], axis=0)
        zdist = alldistance(zplus)
        dist = zdist[0]
        index = np.arange(zplus.shape[0])
        mask = dist > 0
        argmin = np.argmin(dist[mask])
        return index[mask][argmin] - 1

    def __downsample(self, points):
        index = random.sample(range(len(points)), self.limit)
        return [points[i] for i in index]

    def write(self, filename, path=None, names=None):
        z = self.z

        plt.figure()
        plt.scatter(z[:, 0], z[:, 1], color='y')
        plt.scatter(z[self.start, 0], z[self.start, 1], color='orange')
        plt.scatter(z[self.end, 0], z[self.end, 1], color='orange')

        # plt.scatter(z[:, 0], z[:, 1], color='y')
        # plt.scatter(path[1:-1, 0], path[1:-1, 1], color='g')
        # plt.scatter([path[0, 0], path[-1, 0]], [path[0, 1], path[-1, 1]], color='orange')

        if path is not None:
            plt.scatter(path[1:-1, 0], path[1:-1, 1], color='g')
            plt.plot(path[:, 0], path[:, 1], color='g')

        if names is not None:
            for i, label in enumerate(names):
                point = path[i]
                plt.annotate(
                    label,
                    xy=point, xytext=(-20, 20),
                    textcoords='offset points', ha='right', va='bottom',
                    arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

        plt.savefig(filename)
        plt.close()


def read_csv(filename):
    points = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            parts = line.split('|')
            lon, lat, name = float(parts[2]), float(parts[3]), parts[4]
            points.append((lat, lon, name))
    return points
