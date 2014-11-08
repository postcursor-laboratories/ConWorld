#!/usr/bin/env python3

import sys
import png
import value

def create(freqs, amps, octs, seed=None):
    if seed == None:
        seed = 203840           # Keysmash of Grand Worldbuilding
    def noise(x,y):
        val = value.ValueNoise(freqs, amps, octaves=octs, seed=seed).generate(x,y)[0]
        if val < 0:
            print("heightmapper: WARNING: noise for ({},{}) = {} (negative). Clamping to zero.".format(x,y,val))
            val = 0
        elif val > 255:
            print("heightmapper: WARNING: noise for ({},{}) = {} (>255). Clamping to 255.".format(x,y,val))
            val = 255
        return (val,)
    return noise

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
    octaves = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    seed    = int(sys.argv[3]) if len(sys.argv) > 3 else None
    octonly = int(sys.argv[4]) if len(sys.argv) > 4 else None
    octnum  = float(sys.argv[5]) if len(sys.argv) > 5 else 1

    weights = [(1/2)**(i+1) for i in range(octaves)]
    weights = weights[:octaves+1]
    if octonly:
        if octonly < len(weights):
            weights = [weights[i] for i in range(len(weights)) if i == octonly]
        else:
            weights = [octnum if i+1 == octonly else 0 for i in range(octonly)]
    print(weights)
    func = create(weights, weights, len(weights), seed)
    toPNG(func, 1024, 1024).save(sys.argv[1])
