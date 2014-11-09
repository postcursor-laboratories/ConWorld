#!/usr/bin/env python3

import sys
import mapgen

xoffset = -512
yoffset = -512
scale = 80

hm = mapgen._heightmapper
mp = mapgen.transform_addAltitude(hm)

def massive_map_pixel_func(x,y):
    x += xoffset
    y += yoffset

    x *= scale
    y *= scale

    return mp(x,y)

if __name__ == '__main__':
    scale = int(sys.argv[1])
    n = int(sys.argv[2])
    print("generating %d px square map with scale %d" % (n,scale))
    print("estimated time: %ds" % (n**2/256**2*48))
    mapgen.createPNG(massive_map_pixel_func, "massivemap.png", n)
