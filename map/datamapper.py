import pickle 
import os

class DataMap():
    """A data map is any metadata about tiles that requires knowledge of the
    heightmap to generate"""
    def __init__(self, name):
        self.name = name

    def generateTile(self, tileX, tileY, heightmap, size=256):
        pass
    
    def loadTile(self, x,y):
        """Loads a tile from given coordinates"""
        f = open(os.path.join("data", self.name, str(x) + "-" + str(y) + ".data"), 'rb')
        tile = pickle.load(f)
        f.close()
        return tile

    def saveTile(self, tile,x,y):
        """Saves a tile as a pickled data file"""
        path = os.path.join(os.path.dirname(__file__), "data", self.name)
        if not os.path.exists(path):
            os.makedirs(path)
        f = open(os.path.join(os.path.dirname(__file__), "data", self.name, (str(x) + "-" + str(y)))+".data", 'wb')
        pickle.dump(tile, f, 2)
        f.close()

##DEBUG
tile = []
for i in range(255**2):
    tile += [i]

d = DataMap("test")
d.saveTile(tile, 0,0)
d.loadTile(0,0)
