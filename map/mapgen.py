#!/usr/bin/env python3

import heightmapper
import png
import sys

# ==========================================================================================
# GLOBAL CONSTANTS
_octave_weights = [(1/2)**(i+1) for i in range(6)]
print(_octave_weights)
_seed = 203840
_tilesize = 256
_heightmapper = heightmapper.create(_octave_weights, _seed)

_alt_sea   = 64
_alt_beach = _alt_sea+20
_alt_snow  = 200

_color_sea   = [ 60, 60, 200 ]
_color_beach = [ 0xFF, 0xE1, 0xA4 ]
_color_grass = [ 0x00, 0x99, 0x33 ]

# ==========================================================================================
# Pixel transform functions

def transform_addAltitude(heightmap):
    """Adds a color profile and markers to indicate altitude"""
    def transform(x,y):
        height = heightmap(x,y)[0]

        if height <= _alt_sea:
            ret = shift_pixel_towards_value([height]*3, _color_sea, .5)

        elif height > _alt_snow:
            # this scaling factor gives a nice shiny shading around the snow
            #ret = [ min(height*1.1, 255) ]*3
            ret = shift_pixel_towards_value([height]*3, [255]*3, .3)

        elif height > _alt_sea and height <= _alt_beach:
            percent_diff = (height-_alt_sea)/(_alt_beach-_alt_sea)
            shift = .5-.3*percent_diff
            color = shift_pixel_towards_value(_color_beach, _color_grass, percent_diff)
            ret = shift_pixel_towards_value([height]*3, color, shift)

        else:
            ret = shift_pixel_towards_value([height]*3, _color_grass, .25)
        return ret

    return transform

def shift_pixel_towards_value(pixel, value, shift):
    lerp = lambda a, b, w: (1-w)*a + w*b
    ret  = [0]*3
    for i in range(3):
        ret[i] = lerp(pixel[i], value[i], shift)
    return ret

# ==========================================================================================
# Tile generation utilities and raw heightmap

def get_heightmap(tilex, tiley):
    return lambda x, y: _heightmapper(tilex*_tilesize+x, tiley*_tilesize+y)

def generate_tile(tilex, tiley):
    """Generates the tile at position (TILEX, TILEY) and saves it as a .PNG file."""
    hm = get_heightmap(tilex, tiley)
    mp = transform_addAltitude(hm)

    createPNG(mp, "tile-%04d-%04d.png" % (tilex, tiley))
    

def createPNG(pixelfunc, filename):
    """Saves a PNG file as FILENAME, where that PNG is generated with each pixel being
    the output of PIXELFUNC(x,y). PIXELFUNC should be a pure function that returns the
    value at one point.
    
    PIXELFUNC must return a list. The length of the list determines the type of PNG:
        1  ->  greyscale
	2  ->  greyscale with alpha
	3  ->  RGB
	4  ->  RGBA
    """

    v = len(pixelfunc(0,0))
    if v == 1:
        pngmode = "L"
    elif v == 2:
        pngmode = "LA"
    elif v == 3:
        pngmode = "RGB"
    elif v == 4:
        pngmode = "RGBA"
    else:
        raise Exception("Invalid pixelfunc length `%d'!" % v)

    # pngdata is a 2D array; 3D not yet supported in png
    pngdata = []
    for y in range(_tilesize):
        col = []
        for x in range(_tilesize):
            col += pixelfunc(x,y)
        pngdata.append(col)

    png.from_array(pngdata, mode=pngmode).save(filename)

if __name__ == '__main__':
    tilex = int(sys.argv[1])
    tiley = int(sys.argv[2])

    print("Generating tile %d %d" % (tilex, tiley))
    generate_tile(tilex, tiley)
