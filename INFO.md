INFO
=====
Just some general info about how everything works around here.

Tiles are 20m per pixel (20mpp). This means a tile is 5.12km across, or 5120 meters. Assuming that California's missions are a days walk apart from each other, and there is about 30mi≈48.28km between each mission, that means that the walk rate of exploration should be about 48.28/5.12=9.43 tiles/day.

TL;DR
=====
```
def Pixel:
  side = 20*meter
def Tile:
  side = 256*pixel or 5120*meter or 5.12*kilometer
travel_rate = ~10*tiles/day
```
