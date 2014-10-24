import random
import math

def c_mul(a, b):
    return eval(hex((int(a) * b) & 0xFFFFFFFF)[:-1])
def hashtuplesafe(tup):
    value = 0x345678
    for item in tup:
        value = c_mul(1000003, value) ^ hash(item)
    value = value ^ len(tup)
    if value == -1:
        value = -2
    return value
#------------------------------------------------------------------------------ 
# Method 2 from http://lodev.org/cgtutor/randomnoise.html
class ValueNoise:
    """
    frequency - A smaller number generates a more "zoomed-in" terrain with fewer details
    octaves - Smaller number generates more lakes, 0.4 and 10 gives a good result if 320*240 in 2 seconds
    """
    def __init__(self, frequency=0.4, octaves=10.0, seed=0):
        self.frequency = frequency
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
            random.seed(hashtuplesafe((hashtuplesafe(key), hashtuplesafe(key))))
            random.seed(random.randint(0, 0xFFFFFFFF))
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
        value += fractX       * fractY       * self.noise(y1, x1)
        value += fractX       * (1 - fractY) * self.noise(y2, x1)
        value += (1 - fractX) * fractY       * self.noise(y1, x2)
        value += (1 - fractX) * (1 - fractY) * self.noise(y2, x2)

        return value
    def turbulence(self, x, y, size):
        """
        This function controls how far we zoom in/out of the noise array.
        The further zoomed in gives less detail and is more blurry.
        """

        value = 0.0
        initial_size = size

        while size >= 1:
            value += self.smooth_noise(x / size, y / size) * size
            size /= 2.0 #The zooming factor started at 16 here, and is divided through two each time. Keep doing this until the zooming factor is 1

        return 128.0 * value / initial_size #The return value is normalized so that it'll be a number between 0 and 255

    def generate(self, x, y):
        """
        Generate dat value noise, boi
        """

        key = (x, y, self.seed)

        result = self.resultmap
        if key not in result:
            result[key] = int(self.turbulence(x*self.frequency, y*self.frequency, self.octaves))

        return (result[key],)

__all__ = ["ValueNoise"]
