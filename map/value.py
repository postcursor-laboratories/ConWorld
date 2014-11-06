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
def ohhh_someprimes_igetagoodfeeling(tup):
    primes = [9601, 9931, 8693]
    # tup will have three values
    assert len(tup) == 3
    return tup[0] * primes[0] + tup[1] * primes[2] + tup[2] * primes[1]
def randomyish(tup):
    random.seed(tup[0])
    mi = min(tup[1], tup[2])
    ma = max(tup[1], tup[2])
    return random.nextint(mi, ma)
def replwfunc(o):
    if isinstance(o, Number):
        cache = o
        o = lambda i: cache
    elif isinstance(o, Sequence):
        o = o.__getitem__
    return o
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
            random.seed(randomyish(key))
            noise[key] = random.randint(0, 1000) / 1000
        return noise[key]
    def smooth_noise(self, x, y):
        """Returns the average value of the 4 neighbors of (x, y) from the
           noise array."""

        fractX = x - int(x)
        fractY = y - int(y)

        x1 = int(x)
        y1 = int(y)

        x2 = x1 - 1
        y2 = y1 - 1

        #Bilinear interpolation http://en.wikipedia.org/wiki/Bilinear_interpolation
        value = 0.0
        value += fractX       * fractY       * self.noise(x1, y1)
        value += fractX       * (1 - fractY) * self.noise(x1, y2)
        value += (1 - fractX) * fractY       * self.noise(x2, y1)
        value += (1 - fractX) * (1 - fractY) * self.noise(x2, y2)

        return value
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

            # temporary clamp
            if tmp > 255:
                tmp = 255
            if tmp < 0:
                tmp = 0
            result[key] = tmp
        return (result[key],)

__all__ = ["ValueNoise"]
