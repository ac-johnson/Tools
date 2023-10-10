#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 12:09:54 2022

@author: acjohnson16
"""

import numpy as np
from osgeo import gdal,osr
import os
from matplotlib import pyplot as plt



infile = '/home/acjohnson16/Documents/SARtest/S1A_IW_GRDH_1SSH_20170501T080209_20170501T080234_016385_01B20C_BFB6.SAFE/measurement/s1a-iw-grd-hh-20170501t080209-20170501t080234-016385-01b20c-001.tiff'
# infile = '/home/acjohnson16/Documents/SARtest/S1A_IW_20170501T080207_SHP_RTC30_G_gpuned_006D/S1A_IW_20170501T080207_SHP_RTC30_G_gpuned_006D_HH.tif'
outfile = '/home/acjohnson16/Documents/SARtest/S1A_IW_GRDH_1SSH_20170501T080209_20170501T080234_016385_01B20C_BFB6.SAFE/HH_dB_grd.tif'
# outfile = '/home/acjohnson16/Documents/SARtest/S1A_IW_20170501T080207_SHP_RTC30_G_gpuned_006D/test.tif'

# os.system(f'cp {infile} {outfile}')
os.system(f'gdal_translate -of GTiff -ot Float32 {infile} {outfile}')

ds = gdal.Open(outfile, gdal.GA_Update)
data = ds.ReadAsArray()
if len(np.shape(data)) != 2:
    print('DATA NOT THE RIGHT SHAPE!!\nAlso learn to do better error testing and reporting')

olddata = np.array(data)
data[data<1e-6]=1e-6

data = 10*np.log10(data)
# data = 10*np.log10(data**2)-83
data[data==-np.inf]=-60
ds.GetRasterBand(1).WriteArray(data)
ds = None





# ds = gdal.Open("test.tif", GA_Update)
# data = ds.ReadAsArray()

# data[0, 0] = 1

# ds.GetRasterBand(1).WriteArray(data)

# # close the dataset to flush it to disk
# ds = None