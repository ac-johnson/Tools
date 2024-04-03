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
site = 'SlopeMountain'

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


# fbox = [[-148.844929383,69.154343897],
#         [-148.84490879,69.15523914],
#         [-148.842675077,69.155214775],
#         [-148.842678764,69.154323342]] #happy valley
# fboxcenter = [664946,7677215] #happy valley

# fieldsites = ['HV','HVE','IC','SM']
# fieldsitenames = ['Happy Valley','Happy Valley East','Ice Cut','Slope Mountain']
#fieldsitelocs = [[69.15478,-148.84382],[69.15531,-148.83792],[69.04113,-148.83162],[68.43289,-148.94216]]


fieldsites = {'HappyValley':   
         {'site' : 'HV',
          'center' : [-148.84382,69.15478],
          'fieldbox' : [[-148.844929383,69.154343897],
                        [-148.84490879,69.15523914],
                        [-148.842675077,69.155214775],
                        [-148.842678764,69.154323342]]},
    
    'HappyValleyEast':   
             {'site' : 'HVE',
              'center' : [-148.83792,69.15531],
              'fieldbox' : [[-148.839074425,69.154864330],
                            [-148.839027044,69.155759365],
                            [-148.836757989,69.155746693],
                            [-148.836805484,69.154851588]]},
             
    'IceCut':   
             {'site' : 'IC',
              'center' : [-148.83162,69.04113],
              'fieldbox' : [[-148.83260857,69.04065465],
                            [-148.832818731,69.041546254],
                            [-148.830654865,69.041616945],
                            [-148.83044576,69.04072424]]},
             
    'SlopeMountain':   
             {'site' : 'SM',
              'center' : [-148.94216,68.73289],
              'fieldbox' : [[-148.942000691,68.732265882],
                            [-148.943792075,68.732729144],
                            [-148.942386524,68.733467455],
                            [-148.940617115,68.733009025]]}
}


fieldsite = fieldsites[site]

fbox = fieldsite['fieldbox']
fboxcenter = fieldsite['center']
    
fbox = CoordConvert(fbox,'4326',projnum)
fboxcenter = CoordConvert([fboxcenter],'4326',projnum)[0]

#get the x,y index values of point closest to the pixel
xcind = min(range(len(xvc)), key=lambda i: abs(xvc[i]-fboxcenter[0]))
ycind = min(range(len(yvc)), key=lambda i: abs(yvc[i]-fboxcenter[1]))

# fboxx = [i[0] for i in fbox]
# fboxy = [i[1] for i in fbox]
# mxlen = (np.max(fboxx)-np.min(fboxy))

#get max distance between points of field box
maxdist = np.max([np.sqrt((i[0]-j[0])**2+(i[1]-j[1])**2) for i in fbox for j in fbox])

#half windows 
windowx = int(np.ceil(maxdist/np.abs(x_size)))
windowy = int(np.ceil(maxdist/np.abs(y_size)))

cilist = []
cjlist = []
cij = []  #cij is the vector that you really want

fpoly = Polygon(fbox)
farea = fpoly.area
overlap=0

for i in range(ycind-windowy,ycind+windowy):
    for j in range(xcind-windowx,xcind+windowx):
        cilist.append(i)
        cjlist.append(j)
        
        #create a polygon of the box around this area
        square = Polygon([(xve[j], yve[i]), (xve[j+1], yve[i]), 
                          (xve[j+1], yve[i+1]), (xve[j], yve[i+1])])
        
        overlap = square.intersection(fpoly).area
        cij.append(overlap/farea)
        print(f'{i},{j}: {overlap/farea:.3f}')

cilist,cjlist,cij = np.array(cilist),np.array(cjlist),np.array(cij)

np.save(f'boxweights_{fieldsites["site"]}.npy')

from matplotlib import pyplot as plt
plt.figure()
plt.imshow(cij.reshape((4,4)))
plt.colorbar()
    

# squares = [Polygon([(xve[i], yve[j]), (xve[i+1], yve[j]), 
#                     (xve[i+1], yve[j+1]), (xve[i], yve[j+1])])
#                     for i in range(xcind-windowx,xcind+windowx) 
#                     for j in range(ycind-windowy,ycind+windowy)]

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

