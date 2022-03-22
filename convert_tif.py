#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 12:09:54 2022

@author: acjohnson16
"""

import numpy as np
from osgeo import gdal,osr
import os
import glob
# from matplotlib import pyplot as plt



# infile = '/home/acjohnson16/Documents/SARtest/S1A_IW_GRDH_1SSH_20170501T080209_20170501T080234_016385_01B20C_BFB6.SAFE/measurement/s1a-iw-grd-hh-20170501t080209-20170501t080234-016385-01b20c-001.tiff'
# infile = '/home/acjohnson16/Documents/SARtest/S1A_IW_20170501T080207_SHP_RTC30_G_gpuned_006D/S1A_IW_20170501T080207_SHP_RTC30_G_gpuned_006D_HH.tif'
# outfile = '/home/acjohnson16/Documents/SARtest/S1A_IW_GRDH_1SSH_20170501T080209_20170501T080234_016385_01B20C_BFB6.SAFE/HH_dB_grd.tif'
# outfile = '/home/acjohnson16/Documents/SARtest/S1A_IW_20170501T080207_SHP_RTC30_G_gpuned_006D/test.tif'

def converttodb(file):

# os.system(f'cp {infile} {outfile}')
# os.system(f'gdal_translate -of GTiff -ot Float32 {infile} {outfile}')

    ds = gdal.Open(file, gdal.GA_Update)
    data = ds.ReadAsArray()

    data[data<1e-6]=1e-6
    
    data = 10*np.log10(data)
    # data = 10*np.log10(data**2)-83
    data[data==-np.inf]=-60
    ds.GetRasterBand(1).WriteArray(data)
    ds = None

def subtractdb(file1,file2,file3):
    '''file1-file2. Must be in same region. File3 is going to be the output file'''
    # f1t = file1.split('.tif')[0][-50:-42]
    # f2t = file2.split('.tif')[0][-50:-42]
    # f1t = file1.split('.tif')[0][-48:-40]
    # f2t = file2.split('.tif')[0][-48:-40]

    # file3 = f'Diffmap_{f1t}_minus_{f2t}.tif'
    # file3 = f'DiffmapRTC_{f1t}_minus_{f2t}.tif'
    os.system(f'cp {file1} {file3}')
    ds3 = gdal.Open(file3,gdal.GA_Update)
    data3 = ds3.ReadAsArray()
    
    ds2 = gdal.Open(file2)
    data2 = ds2.ReadAsArray()

    # data3 = data3[0] - data2[0]
    data3 = data3 - data2
    # print(np.shape(data3))
    # print(np.shape(data2))
    ds3.GetRasterBand(1).WriteArray(data3)
    
    ds3 = None
    ds2 = None    

if __name__=='__main__':
    doconvert = True
    if doconvert == True:
        imglist = glob.glob('/home/acjohnson16/Documents/SARtest/Kenn_21alt/ASF_RTC_VH/*')
        for img in imglist:
            print(img)
            converttodb(img)
    
    dosub = False
    if dosub==True:
        imglist1 = glob.glob('/home/acjohnson16/Documents/SARtest/Kenn_21/ASF_RTC/*')
        imglist2 = [i.replace('ASF_RTC','ASF_RTC_VH') for i in imglist1]
        imglist2 = [i.replace('VV.tif','VH.tif') for i in imglist2]
        imglist3 = [i.replace('ASF_RTC','subtraction') for i in imglist1]
        imglist3 = [i.replace('VV.tif','VV_minus_VH.tif') for i in imglist3]
        # imglist2 = glob.glob('/home/acjohnson16/Documents/SARtest/Kenn_21/ASF_RTC_VH/*')
        
        for i,img in enumerate(imglist1):
            subtractdb(img, imglist2[i], imglist3[i])
        
# if __name__=='__main__':
#     # print('hello cosmos')
#     dosub=True
#     if dosub==True:
#         # imglist = glob.glob('GEE/*')
#         imglist = glob.glob('ASF_RTC/*align.tif')
#         imlen = len(imglist)
#         for i,img1 in enumerate(imglist):
#             if i<(imlen-1):
#                 for j,img2 in enumerate(imglist[i+1:]):
#                     # print(f'{img1}       {img2}')
#                     subtractdb(img1,img2)


# ds = gdal.Open("test.tif", GA_Update)
# data = ds.ReadAsArray()

# data[0, 0] = 1

# ds.GetRasterBand(1).WriteArray(data)

# # close the dataset to flush it to disk
# ds = None