#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The point of this is to turn the randolph glacier inventory into 
a nice mask.

Things to do:
    
Crop the shapefile to the select area
    I need to extract the extent of these things.
        ok nevermind. It will be easier to reproject the 
Reproject the shapefile to the same EPSG
Then extract the features mappings

These will be:
cropshp - crop, then reproject
createmask - now actually create that mask


Created on Mon Oct  2 12:00:05 2023

@author: acjohnson16
"""

import os
from osgeo import gdal,osr,ogr

def getEPSG(file):
    ds=gdal.Open(file)
    proj = osr.SpatialReference(wkt=ds.GetProjection())
    dsproj = proj.GetAttrValue('AUTHORITY',1)
    ds = None
    return dsproj


# 
#
#
#
#
#
#
#
#





# def clipshp(inshp,)
#we will assume EPSG 4326
# inshpfile = '/home/acjohnson16/Documents/SARtest/RGI_alaska/01_rgi60_Alaska.shp'

# reftiffile = '/home/acjohnson16/Projects/GlacierSAR/data/Kenn/2020/VV/rtc_clipped/S1B_IW_20201024T030324_DVP_RTC30_G_gpuned_A292_VV.tiff'

