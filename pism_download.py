#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is made for downloading PISM data

Created on Thu Mar 17 10:56:00 2022

@author: acjohnson16
"""

import os
import glob

rhost = 'acjohnson16@chinook.alaska.edu'
rfloc = '/import/c1/ICESHEET/ICESHEET/uaf-antarctica/filron/filron_runs/picoruns'
lfloc = '/media/acjohnson16/Clathrate/APModel_util/filron/ens'

os.system('partprobe -d') #Hopefully this will wake up the drive if asleep

# runlist = range(100)
runlist = range(26)
templist = [str(i)+'C' for i in range(7)]
templist.append('rcp26')
templist.append('rcp85')
templist = ['e0C']
# templist=['0C']

resultfull = [f'result_{i}.nc' for i in runlist]
extrafull = [f'extra_{i}.nc' for i in runlist]
tsfull = [f'timeseries_{i}.nc' for i in runlist]

for T in templist:
    print(T)
    resultlist = glob.glob(lfloc+f'/ocean_{T}/result*.nc')
    extralist = glob.glob(lfloc+f'/ocean_{T}/extra*.nc') 
    tslist = glob.glob(lfloc+f'/ocean_{T}/timeseries*.nc') 
    print(f'Runs already downloaded: {len(resultlist)}')

    resultdone = ['result_'+i.split('result_')[1] for i in resultlist]
    extradone = ['extra_'+i.split('extra_')[1] for i in extralist]
    tsdone = ['timeseries_'+i.split('timeseries_')[1] for i in tslist]

    for i in runlist:
        # if i%10==0:
        # print(i)
        rresult = f'{rfloc}/ocean_{T}/output/result_{i}.nc'
        rextra = f'{rfloc}/ocean_{T}/extra/extra_{i}.nc'
        rts = f'{rfloc}/ocean_{T}/extra/timeseries_{i}.nc'
        
        if resultfull[i] not in resultdone:
            # print(f'Copying result_{i}')
            os.system(f'scp -i ~/.ssh/id_rsa.pub {rhost}:{rresult} {lfloc}/ocean_{T}/')
        if extrafull[i] not in extradone:
            if os.path.exists(f'{lfloc}/ocean_{T}/result_{i}.nc'):
                os.system(f'scp -i ~/.ssh/id_rsa.pub {rhost}:{rextra} {lfloc}/ocean_{T}/')
            else:
                print(f'Run {i} extra file exists but result is missing.')
        # if tsfull[i] not in tsdone:
        os.system(f'scp -i ~/.ssh/id_rsa.pub {rhost}:{rts} {lfloc}/ocean_{T}/')