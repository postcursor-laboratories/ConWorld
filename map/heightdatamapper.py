import heightmapper
from datamapper import *

class HeightDataMap(DataMap):
    """Produces a data map of the heightmap at the data.
    For storing the world if perlin suddenly changes"""
    def __init__(self):
        super().__init__("heightmap") #TODO maybe this needs super(args and blah)

    def generate_tile(self, tile_x, tile_y, heightmap, size=32):
        """Produces a datamap of the height at x,y. Only modifies the tile at x,y."""
        tile = Tile(tile_x,tile_y, self, size)
        for y in range(size):
            for x in range(size):
                tile.map[y][x] = heightmap(x,y)
        tile.save()
        return tile

base = .4
count = 15
freqs = []
amps = []
copy = count
done = 0
while done < count:
    freqs.append(base/copy)
    amps.append(copy)
    copy /= 2.0
    done += 1
del copy
del done
_seed = 0xCAFEBABEDEADBEEF
_tilesize = 32
_heightmapper = heightmapper.create(freqs, amps, count, _seed)

def get_heightmap(tilex, tiley, tilesize):
    return lambda x, y: _heightmapper(tilex*tilesize+x, tiley*tilesize+y)

d = HeightDataMap()
d.generate_tile(0, 0, get_heightmap(0,0,32),32)
print(d.tile_exists(0, 0))
print(d.load_tile(0, 0)[16][16])