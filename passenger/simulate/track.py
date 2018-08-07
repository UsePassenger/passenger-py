import itertools
import math

import numpy as np

from passenger.simulate.distance import alldistance, euclidean, haversine


class TrackGenerator(object):
    def __init__(self, osmp, mindist=None, noise_scale=math.inf, eps=1e-8):
        super(TrackGenerator, self).__init__()
        self.osmp = osmp
        self.mindist = mindist
        self.noise_scale = noise_scale
        self.eps = eps

    def nextclosest_helper(self, pointindex, startindex, endindex, z, zdist, mindist=0.2):
        point = z[pointindex]
        start = z[startindex]
        end = z[endindex]

        dist = zdist[pointindex]
        psdist = zdist[startindex, pointindex]
        pedist = zdist[pointindex, endindex]
        sdist = zdist[:, startindex]
        edist = zdist[:, endindex]
        
        index = np.arange(z.shape[0])
        mask = np.logical_and(dist >= 0, np.logical_and(sdist >= psdist, edist <= pedist))
        mask = np.logical_and(mask, dist >= mindist)
        
        dmask = dist[mask]
        imask = index[mask]
        
        argmin = np.argmin(dmask)

        return imask[argmin]

    def nextclosest(self, pointindex, startindex, endindex, z, zdist, mindist=0.3, ntries=3):
        __mindist = mindist
        closest = None
        for i in range(ntries):
            try:
                closest = self.nextclosest_helper(pointindex, startindex, endindex, z, zdist, mindist=__mindist)
            except:
                __mindist = mindist - (mindist / ntries) * (i+1)
        return closest

    def generate(self):
        mindist = self.mindist
        noise_scale = self.noise_scale
        eps = self.eps

        z = self.osmp.z

        zdist = alldistance(z)

        start = z[self.osmp.start]
        startindex = self.osmp.start
        end = z[self.osmp.end]
        endindex = self.osmp.end

        closest = start
        nextindex = startindex
        pathindex = [startindex]

        count = 0

        for _ in itertools.repeat(None):
            noise = np.random.normal(size=1, scale=mindist/noise_scale)
            __mindist = mindist + noise

            prevclosest = closest
            
            nextindex = self.nextclosest(nextindex, startindex, endindex, z, zdist, mindist=__mindist)
            
            if nextindex is None:
                nextindex = endindex
            
            closest = z[nextindex]

            # TODO: Use haversine.
            prev2now = euclidean(prevclosest, closest)
            prev2end = euclidean(prevclosest, end)

            if prev2now + eps >= prev2end:
                nextindex = endindex
                closest = end
            
            pathindex.append(nextindex)
            
            if nextindex == endindex:
                break

            count += 1

            if count > z.shape[0]:
                raise RuntimeError('Loop did not terminate.')

        path = z[pathindex]
        
        return path, pathindex

    
    def generate_track(z, start_index=None, end_index=None, mindist=0.6, noise_scale=10):
        """
        mindist = 0.6
        noise_scale = 10  # use math.inf to ignore
        """
        
        if start_index is None:
            print('setting start_index')
            start_index = 0
        if end_index is None:
            print('setting end_index')
            end_index = z.shape[0] - 1
        
        start = z[start_index]
        end = z[end_index]

        zdist = alldistance(z)

        path, pathindex = heuristic_path(start_index, end_index, z, zdist, mindist=mindist, noise_scale=noise_scale)

        print('Path Length = {}'.format(path.shape[0]))
        
        return path, pathindex