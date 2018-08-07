import numpy as np


def alldistance(z):
    zdiff = z.reshape(-1, 1, 2) - z.reshape(1, -1, 2)
    zexp = np.power(zdiff, 2)
    zagg = np.sum(zexp, 2)
    zroot = np.sqrt(zagg)
    return zroot


def euclidean(a, b):
    diff = a - b
    exp = np.power(diff, 2)
    agg = np.sum(exp)
    root = np.sqrt(agg)
    return root


def haversine(lat1, lon1, lat2, lon2, scale=3961):
    """
    The haversine distance is used to find the distance between two points on a sphere.
    
    scale is an approx. radius of the earth in miles
    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    dist = scale * c
    return dist
