#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 10:47:01 2022

@author: acjohnson16
"""

from zipfile import ZipFile
# import zipfile
import glob
import os
import shutil


def extracttif(inloc,outloc,pol='VV'):

    infile = glob.glob(f'{inloc}*')
    endstr = pol+'.tif'
    for file in infile:
        # print(file)
        # namelist = 
        with ZipFile(file) as z:
            z = ZipFile(file)
            zname = [name for name in z.namelist() if name[-6:]==endstr][0]
            # z.extract()
        
            filename = os.path.basename(zname)
            source = z.open(zname)
            target = open(os.path.join(outloc, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)

if __name__=='__main__':
    dirname = 'Greenland_test1'
    pol = 'HV'
    
    inloc = f'/home/acjohnson16/Documents/SARtest/{dirname}/indata/'
    outloc = f'/home/acjohnson16/Documents/SARtest/{dirname}/ASF_RTC{"" if (pol=="VV" or pol=="HH") else "_"+pol}/'
    
    # inloc = '/home/acjohnson16/Documents/SARtest/Kenn_21alt/indata/'
    # outloc = '/home/acjohnson16/Documents/SARtest/Kenn_21alt/ASF_RTC_VH/'
    
    extracttif(inloc, outloc, pol)