#!/usr/bin/env python3

import sys
import png
import value

def create(octave_weights, seed=None):
    if seed == None:
        seed = 203840           # Keysmash of Grand Worldbuilding
    return value.ValueNoise(.01, octaves=len(octave_weights), seed=seed).generate

def toPNG(func, xsize, ysize):
    pngdata = []
    for y in range(ysize):
        col = []
        for x in range(xsize):
            res = func(x, y)[0]
            col.append(res)
        pngdata.append(col)

    # L makes it greyscale
    return png.from_array(pngdata, mode="L")

if __name__ == '__main__':
    if len(sys.argv) < 2 or '--help' in sys.argv or '-h' in sys.argv:
        print('2dtexture.py FILE [OCTAVES] [SEED] [OCTAVE_ONLY] [OCTAVE_ONLY_NUMBER]')
        print()
        print(__doc__)
        exit()
    
    #weights = [.1, .1, .2, .3, .5, 1]
    #weights = [0, 0, 0, 0, 1]
    octaves = int(sys.argv[2]) if len(sys.argv) > 2 else None
    seed    = int(sys.argv[3]) if len(sys.argv) > 3 else None
    octonly = int(sys.argv[4]) if len(sys.argv) > 4 else None
    octnum  = float(sys.argv[5]) if len(sys.argv) > 5 else None

    weights = [(1/2)**(i+1) for i in range(octaves)]
    weights = weights[:octaves+1]
    if octonly:
        if octonly < len(weights):
            weights = [weights[i] for i in range(len(weights)) if i == octonly]
        else:
            weights = [octnum if i+1 == octonly else 0 for i in range(octonly)]
    print(weights)
    func = create(weights, seed)
    toPNG(func, 1024, 1024).save(sys.argv[1])
