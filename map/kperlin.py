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
        return self.noise.get(coords)
    def __setgen(self, x, y, gen):
        self.noise[(x, y)] = gen
        return gen
    def getnoise(self, x, y):
        loc = (x, y)
        if loc not in self:
            self.noise[loc] = self.noise2(x, y)
        return self.noise[loc]
    @abstractmethod
    def noise2(self, x, y):
        pass

class Perlin(NoiseGenerator2D):
    def __init__(self, seed, octaves=1, persistence=1):
        super().__init__()
        self.n = octaves
        if isinstance(persistence, Number):
            cache = persistence
            persistence = lambda i: cache
        elif isinstance(persistence, Sequence):
            persistence = persistence.__getitem__
        self.p = persistence
        self.seed = seed
        self.rawnoise = {}
        self.define_inoise(seed)
    def define_inoise(self, seed):
        self.rawnoise = {}
        self.rawsnoise = {}
        self.rawinoise = {}
        def noise(x, y):
            loc = (x, y)
            if loc not in self.rawnoise:
                n = x + y * 2147483647 + seed
                random.seed(n)
                sign = random.randint(0, 1) == 1
                self.rawnoise[loc] = (-1 if sign else 1) * random.random()
            return self.rawnoise[loc]
        def snoise(x, y):
            loc = (x, y)
            if loc not in self.rawsnoise:
                corners = (noise(x - 1, y - 1) + noise(x + 1, y - 1) + noise(x - 1, y + 1) + noise(x + 1, y + 1)) / 16
                sides   = (noise(x - 1, y) + noise(x + 1, y) + noise(x, y - 1) + noise(x, y + 1)) /  8
                center  =  noise(x, y) / 4
                self.rawsnoise[loc] = corners + sides + center
            return self.rawsnoise[loc]
        def inoise(x, y):
            loc = (x, y)
            if loc not in self.rawinoise:
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
                self.rawinoise[loc] = interpolate(i1 , i2 , fy)
            return self.rawinoise[loc]
        self.inoise = inoise
    def noise2(self, x, y):
        persist_out = [self.p(i) for i in range(self.n)]
        persist_sum = sum(persist_out)
        persist_balanced = [i/persist_sum for i in persist_out]
        return sum(self.inoise(x * 2**i, y * 2**i) * persist_balanced[i]**i for i in range(self.n))

__all__ = ["NoiseGenerator2D", "Perlin"]
