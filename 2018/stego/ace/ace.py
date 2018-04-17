#!/usr/bin/env python3
from PIL import Image

# you'll need to Pillow package to run this
# "pip3 install Pillow" should work, otherwise see
# https://pillow.readthedocs.io/en/3.0.x/installation.html

img = Image.new('RGB', (600,100))
img_data = [None for x in range(600*100)]
# the file names are hardcoded because it just isn't worth the effort
with open('ace.txt', 'r') as f:
    for line in f.readlines():
        try:
            color,coords = line.split()
            x,y = coords.split(',')
            x,y = int(x),int(y)
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:], 16)
            img_data[(y*600)+x] = (r,g,b)
        except IndexError:
            print(x,y)
            exit()
    img.putdata(img_data)
    img.save('ace.png')
