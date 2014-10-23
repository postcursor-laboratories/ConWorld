from abc import *
from numbers import Number
from collections import Sequence
import random

def interpolate(a, b, x, xmin=0, xmax=1):
    return a * (xmax - x) + b * (x - xmin)

class NoiseGenerator2D:
    __metaclass__  = ABCMeta
    X1 = 0
    Y1 = 1
    X2 = 2
    Y2 = 3
    def __init__(self):
        self.width = 0
        self.height = 0
        self.originx = 0
        self.originy = 0
        self.noise = {}
    def __contains__(self, coords):
        x = coords[X1]
        y = coords[Y1]
        xdict = self.noise.get(x)
        if xdict and xdict.get(y):
            return True
        return False
    def __setgen(self, x, y, gen):
        if not x in self.noise:
            self.noise[x] = {}
        self.noise[x][y] = gen
        return gen
    def getnoise(self, x, y):
        if (x, y) in self:
            return self.noise[x][y]
        gen = noise2(x, y)
        return self.__setgen(x, y, gen)
    @abstractmethod
    def noise2(self, x, y):
        pass

class Perlin(NoiseGenerator2D):
    def __init__(self, seed, octaves=1, persistence=1):
        self.n = octaves
        if isinstance(persistence, Number):
            cache = persistence
            persistence = lambda i: cache
        elif isinstance(persistence, Sequence):
            persistence = persistence.__getitem__
        self.p = persistence
        self.seed = seed
        self.define_inoise(seed)
    def define_inoise(self, seed):
        def noise(x, y):
            n = x + y * 2147483647 + seed
            random.seed(n)
            sign = random.randint(0, 1) == 1
            return (-1 if sign else 1) * random.random()
        def snoise(x, y):
            corners = (noise(x - 1, y - 1) + noise(x + 1, y - 1) + noise(x - 1, y + 1) + noise(x + 1, y + 1)) / 16
            sides   = (noise(x - 1, y) + noise(x + 1, y) + noise(x, y - 1) + noise(x, y + 1)) /  8
            center  =  noise(x, y) / 4
            return corners + sides + center
        def inoise(x, y):
            ix = int(x)
            fx = x - ix
            iy = int(y)
            fy = y - iy

            v1 = snoise(ix, iy)
            v2 = snoise(ix + 1, iy)
            v3 = snoise(ix, iy + 1)
            v4 = snoise(ix + 1, iy + 1)

            i1 = interpolate(v1 , v2 , fx)
            i2 = interpolate(v3 , v4 , fx)
            return interpolate(i1 , i2 , fy)
        self.inoise = inoise
    def noise2(self, x, y):
        return sum(self.inoise(x * 2**i, y * 2**i) * self.p(i)**i for i in range(self.n))

__all__ = ["NoiseGenerator2D", "Perlin"]
