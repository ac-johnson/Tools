#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lots of the functions here are just copied from coordconvert. This is a better
place to organize them.

Created on Mon Apr  1 14:36:08 2024

@author: acjohnson16
"""

from osgeo import gdal,osr
import numpy as np

def getEPSG(file):
    ds=gdal.Open(file)
    proj = osr.SpatialReference(wkt=ds.GetProjection())
    dsproj = proj.GetAttrValue('AUTHORITY',1)
    ds = None
    return dsproj

def getProjection(file):
    ds = gdal.Open(file)
    proj = osr.SpatialReference(wkt=ds.GetProjection())
    return proj

def coordConvert(points,inproj,outproj,ptparse=False):
    """Convert coordinate grid from one projection to another
    if converting from 4326, then points should be ordered lon,lat"""

    if ptparse:
        points = wtkparse(points)

    if type(inproj)==str:
        inproj=int(inproj)
    if type(outproj)==str:
        outproj=int(outproj)

    epsgin = osr.SpatialReference()
    epsgin.ImportFromEPSG(inproj)   
    epsgout = osr.SpatialReference()
    epsgout.ImportFromEPSG(outproj)

    convert = osr.CoordinateTransformation(epsgin, epsgout)
    points = np.array(points)
    
    for i,x in enumerate(points):
        newpt = convert.TransformPoint(x[1],x[0])
        points[i,0],points[i,1]=newpt[0],newpt[1]
        
    return points

def makeWKT(tl,sz,useproj,inproj=4326,outproj=4326):
    """makes a WKT string based on a point
    tl gives top left point, sz is the size of the box in m
    useproj is a utm projection to use
    inpoints should be ordered lon,lat"""


    #create the box in UTM
    tl = coordConvert([tl],inproj=inproj,outproj=useproj)[0]
    tl = [tl[0],tl[1]]
    tlx,tly = tl[0],tl[1]
    tr = [tlx+sz,tly]
    br = [tlx+sz,tly-sz]
    bl = [tlx,tly-sz]
    box = [tl,tr,br,bl,tl]

    #convert box back to latlon and make string
    wktstr = 'POLYGON(('
    for bb in box:
        # print(bb[0])
        bo = coordConvert([[bb[1],bb[0]]],useproj,outproj)
        plat,plon = bo[0]
        # print(plat)
        # print(bo[0][0])
        # box[i]=bo
        wktstr = wktstr + f'{plon:.4f} {plat:.4f},'
    wktstr = wktstr[:-1]
    wktstr = wktstr+'))'
    return wktstr
    
    #makestring
    # wktstr = 'POLYGON(('
    # for bb in box:
        
    
if __name__=='__main__':
    # pt = [476291.365240411, 7223664.829083515] #poker for 3km
    pt = [-147.505331, 65.135626]   #poker flat 3 km
    print(makeWKT(pt,3000,32606))
    # print(wkt)

    pt = [-147.911426, 64.874897]   #campus area 3 km
    print(makeWKT(pt,3000,32606))

# def 