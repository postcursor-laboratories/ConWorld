#!/usr/bin/env python3

import sys
import png
import random
from noise import snoise2

def create(octaves, seed=None):
    # TODO: make the seed actually work!
    if seed:
        random.seed(seed)
        #snoise.randomize()

    freq = 16.0*octaves
    def get(x,y):
        return int(snoise2(x/freq, y/freq, octaves)*127.0 + 128.0)
    return get

def toPNG(func, xsize, ysize):
    pngdata = []
    for y in range(ysize):
        col = []
        for x in range(xsize):
            col.append(func(x,y))
        pngdata.append(col)

    # L makes it greyscale
    return png.from_array(pngdata, mode="L")

if __name__ == '__main__':
    if len(sys.argv) not in range(2,5) or '--help' in sys.argv or '-h' in sys.argv:
        print('2dtexture.py FILE [OCTAVES] [SEED]')
        print()
        print(__doc__)
        raise SystemExit

    if len(sys.argv) > 2:
        octaves = int(sys.argv[2])
    else:
        octaves = 1

    if len(sys.argv) > 3:
        seed = int(sys.argv[3])
    else:
        seed = None
    
    func = create(octaves, seed)
    toPNG(func, 256, 256).save(sys.argv[1])
