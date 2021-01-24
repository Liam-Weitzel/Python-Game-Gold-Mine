import random

map_width = 30
map_height = 100
grasslevel = 5

map = [ [0]*map_width for i in range(map_height)]

for h in range(0, map_height):
  for w in range(0, map_width):
    if (h > grasslevel):
      r = random.random();
      if (r > 0.75): #ore or blank tile
          if (r > 0.98):
            map[h][w] = 5
          elif (r > 0.95):
            map[h][w] = 4
          elif (r > 0.90):
            map[h][w] = 3
          elif (r > 0.75):
            map[h][w] = 0
      else: #dirt tile
          map[h][w] = 1
    elif (h == grasslevel): #grass tile
      map[h][w] = 2
    elif (h < grasslevel): #border blocker
      if (w == 0 or w == map_width-1):
          map[h][w] = 7
      else:
          map[h][w] = 0

maptxtfile = open('map.txt','w')

for h in range(0, map_height):
  print("test")
  for w in range(0, map_width):
    maptxtfile.write(str(map[h][w]))
  maptxtfile.write('\n')

maptxtfile.close()
