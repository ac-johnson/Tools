#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 12:12:15 2024

@author: acjohnson16
"""

import numpy as np
from osgeo import gdal
from shapely.geometry import Polygon
from geo_utils import getEPSG,CoordConvert
# from coordconvert import getEPSG,CoordConvert

#first task is function for getting the xy vects or grid

file = '/home/acjohnson16/Projects/GIS/area/S1AA_20230627T164402_20230709T164403_VVP012_INT80_G_ueF_93ED_amp.tiff'

projnum = getEPSG(file)

#get XY vectors
r = gdal.Open(file)
# band = r.GetRasterBand(1)

(upper_left_x, x_size, x_rotation, upper_left_y, y_rotation, y_size) = r.GetGeoTransform()
# print(r.GetGeoTransform())
asz = np.shape(r.ReadAsArray())
# asz

xvc = np.arange(upper_left_x,upper_left_x+x_size*asz[1],x_size) #center points of pixels
xve = np.arange(upper_left_x-x_size/2,upper_left_x+x_size*asz[1]+x_size/2,x_size) #edges

yvc = np.arange(upper_left_y,upper_left_y+y_size*asz[0],y_size) #center points of pixels
yve = np.arange(upper_left_y-y_size/2,upper_left_y+y_size*asz[0]+y_size/2,y_size) #edges


fbox = [[-148.844929383,69.154343897],
        [-148.84490879,69.15523914],
        [-148.842675077,69.155214775],
        [-148.842678764,69.154323342]] #happy valley
fboxcenter = [664946,7677215] #happy valley

fbox = CoordConvert(fbox,'4326','32605')

#get the x,y index values of point closest to the pixel
xcind = min(range(len(xvc)), key=lambda i: abs(xvc[i]-fboxcenter[0]))
ycind = min(range(len(yvc)), key=lambda i: abs(yvc[i]-fboxcenter[1]))

# fboxx = [i[0] for i in fbox]
# fboxy = [i[1] for i in fbox]
# mxlen = (np.max(fboxx)-np.min(fboxy))

#get max distance between points
maxdist = np.max([np.sqrt((i[0]-j[0])**2+(i[1]-j[1])**2) for i in fbox for j in fbox])

#half windows 
windowx = int(np.ceil(maxdist/np.abs(x_size))+1)
windowy = int(np.ceil(maxdist/np.abs(y_size))+1)

squares = [Polygon([(xve[i], yve[j]), (xve[i+1], yve[j]), 
                    (xve[i+1], yve[j+1]), (xve[i], yve[j+1])])
                    for i in range(xcind-windowx,xcind+windowx) 
                    for j in range(ycind-windowy,ycind+windowy)]

# test = [[(xve[i], yve[j]), (xve[i+1], yve[j]), 
#                     (xve[i+1], yve[j+1]), (xve[i], yve[j+1])]
#                     for i in range(xcind-windowx,xcind+windowx) 
#                     for j in range(ycind-windowy,ycind+windowy)]



# test = Polygon(fbox)
# xcind = xvc.index(np.abs)


#seek to restore honor
#our your tea



# def fieldbox_to_utm(fbox,epsgn):
#     newbox = []
#     for pt in fbox:
#         CoordConvert


# # Define the squares in a 3x3 grid. Each square is a Shapely polygon.
# squares = [Polygon([(x, y), (x+1, y), (x+1, y+1), (x, y+1)]) for x in range(3) for y in range(3)]

# # Define the parallelogram by its vertices as a Shapely polygon.
# parallelogram = Polygon([(0.5, 0.5), (2.0, 0.5), (2.5, 1.8), (1, 1.8)])

# # Calculate the intersection area of each square with the parallelogram.
# overlap_areas = [square.intersection(parallelogram).area for square in squares]

# # Print the overlap areas.
# for i, area in enumerate(overlap_areas, 1):
#     print(f"Square {i}: {area} units²")
