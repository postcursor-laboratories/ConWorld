import pickle 
import os

class DataMap():
    """A data map is any metadata about tiles that requires knowledge of the
    heightmap to generate"""
    def __init__(self, name):
        self.name = name

    def generate_tile(self, tileX, tileY, heightmap, size=256):
        """This is the main part of a DataMap and will be overwritten by most superclasses.
        Generating a tile should effect at most the tiles 2 away from it.
        NOTE: This does not make a tile ready for use. Generate tile may modify tiles up to 2 away
        and before unhiding a tile make sure all tiles 2 away have been propagated."""
        tile = Tile(tileX, tileY, self, size)
        for y in range(size):
            for x in range(size):
                tile.map[y][x] = x+y
        tile.save()
        return tile

    def tile_exists(self, x,y):
        """returns true iff file with name exists. TODO make it so you can't mess it up with a fake file."""
        return os.path.exists(os.path.join("data", self.name, str(x) + "-" + str(y) + ".data"))
    
    def load_tile(self, x,y):
        """Loads a tile from given coordinates
        THROWS file not found gloop if there isn't a file. use tile_exists()
        to check."""
        f = open(os.path.join("data", self.name, str(x) + "-" + str(y) + ".data"), 'rb')
        tile = pickle.load(f)
        f.close()
        return tile

    def save_tile(self, tile,x,y):
        """Saves a tile as a pickled data file"""
        path = os.path.join(os.path.dirname(__file__), "data", self.name)
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(os.path.join(os.path.dirname(__file__), "data", self.name, (str(x) + "-" + str(y)))+".data", 'wb')
        pickle.dump(tile, f, 2)
        f.close()

class Tile():
    """Stores a 2d array of... anything, I guess. Also holds it's x, y, and status of generation."""
    def __init__(self, x, y, parent, overwrite = False, size = 256):
        if not parent.tile_exists(x,y) or overwrite: # If tile has never been created or we want force overwrite
            self._x = x
            self._y = y
            self.size = size
            self.map = []
            for i in range(size):
                self.map += [[]]
                for j in range(size):
                    self.map[i] += [0]
            self.parent = parent

            self._state = 0 #0: completely ungenerated.
                            #1: has some generation but has not generated itself yet. eg rivers flow in, but no springs
                            #2: has generated itself but some tiles may still modify it.
                            #3: completely defined, all tiles around it cannot modify it anymore.
        else:
            self = parent.load_tile(x,y) # Tile already exists and we don't want to overwrite

    def save(self):
        """Saves this tile as a pickled data file"""
        path = os.path.join(os.path.dirname(__file__), "data", self.parent.name)
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(os.path.join(os.path.dirname(__file__), "data", self.parent.name, (str(self._x) + "-" + str(self._y)))+".data", 'wb')
        pickle.dump(self.map, f, 2)
        f.close()
