#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 10:20:20 2022

@author: acjohnson16
"""

from osgeo import gdal, gdalconst
import glob
# import os

def aligntif(file,reffile):
    '''Aligns file to a reference file, and saves it'''
    
    # inputfile = #Path to input file
    input = gdal.Open(file, gdalconst.GA_ReadOnly)
    inputProj = input.GetProjection()
    inputTrans = input.GetGeoTransform()
    
    reference = gdal.Open(reffile, gdalconst.GA_ReadOnly)
    referenceProj = reference.GetProjection()
    referenceTrans = reference.GetGeoTransform()
    bandreference = reference.GetRasterBand(1)    
    x = reference.RasterXSize 
    y = reference.RasterYSize
    
    outputfile = file.split('.tif')[0]+'_align.tif'
    
    # outputfile = #Path to output file
    driver= gdal.GetDriverByName('GTiff')
    output = driver.Create(outputfile, x, y, 1, bandreference.DataType)
    output.SetGeoTransform(referenceTrans)
    output.SetProjection(referenceProj)
    
    gdal.ReprojectImage(input, output, inputProj, referenceProj, gdalconst.GRA_Bilinear)
    
    del output


if __name__ == '__main__':
    # infile = '/home/acjohnson16/Documents/SARtest/Ronne_Jul21/ASF_RTC/S1A_IW_20210703T062714_SHP_RTC30_G_gpuned_F6C6_HH.tif'
    # reffile = '/home/acjohnson16/Documents/SARtest/Ronne_Jul21/ASF_RTC/S1A_IW_20210704T021606_SHP_RTC30_G_gpuned_E0DB_HH.tif'
    
    # aligntif(infile,reffile)
    
    flist = glob.glob('/home/acjohnson16/Documents/SARtest/Ronne_Jul21/ASF_RTC/*')
    reftif = flist[-1]
    flist = flist[:-1]
    for file in flist:
        print(file)
        aligntif(file,reftif)
    