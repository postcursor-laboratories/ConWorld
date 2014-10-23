#!/usr/bin/env python3

import sys
import png
import perlin

def create(octave_weights, seed=None):
    if not seed:
        seed = 203840           # Keysmash of Grand Worldbuilding
    return perlin.perlin_noise(seed, octave_weights)

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

    weights = [.1, .1, .2, .3, .5, 1]
    func = create(weights[:octaves], seed)
    toPNG(func, 1024, 1024).save(sys.argv[1])
