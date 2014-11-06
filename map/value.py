from numbers import Number
from collections import Sequence
import random
import math

def hashtuplesafe(tup):
    value = 0x345678
    for item in tup:
        value = (1000003 * value) ^ item
    value = value ^ len(tup)
    return value
def replwfunc(o):
    if isinstance(o, Number):
        cache = o
        o = lambda i: cache
    elif isinstance(o, Sequence):
        o = o.__getitem__
    return o
def bilinear_interpolation(x, y, points):
    '''Interpolate (x,y) from values associated with four points.

    The four points are a list of four triplets:  (x, y, value).
    The four points can be in any order.  They should form a rectangle.

        >>> bilinear_interpolation(12, 5.5,
        ...                        [(10, 4, 100),
        ...                         (20, 4, 200),
        ...                         (10, 6, 150),
        ...                         (20, 6, 300)])
        165.0

    '''
    # See formula at:  http://en.wikipedia.org/wiki/Bilinear_interpolation

    points = sorted(points)               # order points by x, then by y
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')

    return (q11 * (x2 - x) * (y2 - y) +
            q21 * (x - x1) * (y2 - y) +
            q12 * (x2 - x) * (y - y1) +
            q22 * (x - x1) * (y - y1)
           ) / ((x2 - x1) * (y2 - y1) + 0.0)
#------------------------------------------------------------------------------ 
# Method 2 from http://lodev.org/cgtutor/randomnoise.html
class ValueNoise:
    """
    frequency - A smaller number generates a more "zoomed-in" terrain with fewer details
    octaves - Smaller number generates more lakes, 0.4 and 10 gives a good result if 320*240 in 2 seconds
    """
    def __init__(self, frequency=0.4, amplitude=1, octaves=10.0, seed=0):
        self.frequency = replwfunc(frequency)
        self.amplitude = replwfunc(amplitude)
        self.octaves = octaves
        self.seed = seed
        self.random = random.Random()
        self.noisemap = {}
        self.resultmap = {}
        self.xycmap = {}
    def noise(self, x, y):
        key = (x, y, self.seed)
        noise = self.noisemap
        if key not in noise:
            random.seed(hashtuplesafe(key))
            noise[key] = random.randint(0, 1000) / 1000
        return noise[key]
    def smooth_noise(self, x, y):
        """Returns the average value of the 4 neighbors of (x, y) from the
           noise array."""
        x1 = int(x)
        y1 = int(y)
        x2 = x1 - 1
        y2 = y1 - 1

        #Bilinear interpolation http://en.wikipedia.org/wiki/Bilinear_interpolation
        x1y1 = (x1, y1, self.noise(x1, y1))
        x1y2 = (x1, y2, self.noise(x1, y2))
        x2y1 = (x2, y1, self.noise(x2, y1))
        x2y2 = (x2, y2, self.noise(x2, y2))

        return bilinear_interpolation(x, y, [x1y1, x1y2, x2y1, x2y2])
    def generate(self, x, y):
        """
        Generate dat value noise, boi
        """

        key = (x, y, self.seed)

        result = self.resultmap
        if key not in result:
            tmp = 0
            for n in range(self.octaves):
                f = self.frequency(n)
                a = self.amplitude(n)
                tmp += self.smooth_noise(x*f, y*f)*a
            tmp /= self.octaves
            tmp *= 128

            result[key] = tmp
        return (result[key],)

__all__ = ["ValueNoise"]
