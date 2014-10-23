from abc import *

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
    def __init__(self, octaves=1, persistance=1):
        self.n = octave
        self.p = persistance
        def noise(x, y):
            n = x + y * 57
            n = (n << 13) ^ n
            return (1.0 - (n * (n * n *  15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0)
        def snoise(x, y)
            corners = (noise(x - 1, y - 1) + noise(x + 1, y - 1) + noise(x - 1, y + 1) + noise(x + 1, y + 1)) / 16
            sides   = (noise(x - 1, y) + noise(x + 1, y) + noise(x, y - 1) + noise(x, y + 1)) /  8
            center  =  noise(x, y) / 4
            return corners + sides + center
        def inoise(x, y)
            ix = int(x)
            fx = x - ix
            iy = int(y)
            fy = y - fy

            v1 = snoise(ix, iy)
            v2 = snoise(ix + 1, iy)
            v3 = snoise(ix, iy + 1)
            v4 = snoise(ix + 1, iy + 1)

            i1 = interpolate(v1 , v2 , fx)
            i2 = interpolate(v3 , v4 , fx)
            return interpolate(i1 , i2 , ft)
        self.inoise = inoise
    def noise2(self, x, y):
        return sum(self.inoise(x * i * 2) * self.p * i for i in range(self.n))
           
__all__ = ["Perlin"]
