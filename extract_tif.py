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

inloc = '/home/acjohnson16/Documents/SARtest/Kenn_21/indata/'
outloc = '/home/acjohnson16/Documents/SARtest/Kenn_21/ASF_RTC/'

infile = glob.glob(f'{inloc}*')
for file in infile:
    # print(file)
    # namelist = 
    with ZipFile(file) as z:
        z = ZipFile(file)
        zname = [name for name in z.namelist() if name[-6:]=='VV.tif'][0]
        # z.extract()
    
        filename = os.path.basename(zname)
        source = z.open(zname)
        target = open(os.path.join(outloc, filename), "wb")
        with source, target:
            shutil.copyfileobj(source, target)