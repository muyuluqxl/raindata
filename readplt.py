# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 23:25:21 2023

@author: shali
"""

import os
import h5py
import numpy as np
import pickle
import glob
import scipy.io as scio
from   copy import copy
#from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from   cartopy.io.img_tiles import Stamen
import cartopy.feature as cfeature
from   cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import shapely.geometry as sgeom
import cartopy.io.shapereader as shpreader
from   matplotlib.patches import RegularPolygon
from   matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from   matplotlib import colors, cm
import matplotlib as mpl
from   sklearn.datasets import load_iris
from   sklearn.preprocessing import StandardScaler


# load map file
fname='./shp/china.shp'
guojie=list(shpreader.Reader(fname).geometries())

""" fname_1='D:/my-project/fengyun/map/ChinaProv.shp'
shengjie=list(shpreader.Reader(fname_1).geometries()) """

data = scio.loadmat("E:/code/python/gis/frykit/frykit/data/PRE_1961_2022_summer.mat")
pre_06 = data['pre_06']
Lat = data['Lat']*0.01
Lon = data['Lon']*0.01
x,y,z = pre_06.shape
pre_06_mean1 = np.zeros((x,y,z),dtype=np.float64)
pre_06_mean = np.nanmean(pre_06, axis = 2)
for i in range(z):
    pre_06_mean1[:,:,i] = pre_06_mean[:,:]

pre_06_anomal = (pre_06 - pre_06_mean1)/pre_06_mean1
pre_06_anomal = pre_06_anomal * 100
fig     = plt.figure(figsize=(9,9))
#fig.subplots_adjust(left=0.05, right=0.95)
ax1 = fig.add_axes([0.1, 0.1, 0.75, 0.94],projection=ccrs.PlateCarree())
ax1.set_extent([65,140,5,48])
ax1.coastlines(resolution='10m')
ax1.add_geometries(guojie,ccrs.PlateCarree(),edgecolor='black',facecolor='white',alpha=1,lw=2.2) 
ax1.add_feature(cfeature.RIVERS.with_scale('50m'),edgecolor='black',facecolor='white',alpha=0.5,lw=1.2)
ax1.add_feature(cfeature.LAKES.with_scale('50m'),edgecolor='black',facecolor='white',alpha=0.5,lw=1.2)
tiler  = Stamen('terrain-background')
#bounds = np.arange(0,10,1)
bounds = [0,2,3,4,5,6,7,9,126,127]
#cmap = mpl.colors.ListedColormap( ['darkorchid','gold','royalblue','cyan','hotpink','lime'])
cmap = mpl.colors.ListedColormap( ['lightcyan','blue','lightseagreen','mediumspringgreen','crimson','m','lawngreen','goldenrod',
                                   'grey','k'])
col= ['lightcyan','blue','lightseagreen','mediumspringgreen','crimson','m','lawngreen','goldenrod',
                                   'grey','k']
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

im1=plt.scatter(Lon,Lat,c=pre_06_mean1[:,1,1],cmap=cmap,s=5,marker='s',
                transform=ccrs.PlateCarree(),alpha=1,norm=norm)
#im1=plt.contourf(lon1, lat1,CLT,cmap=cmap,transform=ccrs.PlateCarree(),levels=bounds)
#im1=plt.contour(lon1,lat1,c=CLT,cmap=cmap,s=100,marker='s',
#                transform=ccrs.PlateCarree(),alpha=0.8,norm=norm)
#im1=plt.pcolormesh(lon1,lat1,CLT,transform=ccrs.Orthographic(),cmap=cmap, norm=norm,alpha=1)
ax1.coastlines()
ax1.spines['geo'].set_linewidth(2)
ax1.set_xlabel([])
ax1.set_ylabel([])
gl=ax1.gridlines(draw_labels=True,linestyle="--",linewidth=1,color=[0.4,0.4,0.4])
gl.top_labels=False #关闭上部经纬标签                                  
gl.right_labels=False
gl.xformatter = LONGITUDE_FORMATTER  #使横坐标转化为经纬度格式            
gl.yformatter = LATITUDE_FORMATTER                                        
gl.xlocator=mticker.FixedLocator([])      
gl.ylocator=mticker.FixedLocator([]) 
gl.xlocator=mticker.FixedLocator([75,95,115,135])      
gl.ylocator=mticker.FixedLocator([5,15,25,35,45]) 
gl.xlabel_style={'size':15}#修改经纬度字体大小                             
gl.ylabel_style={'size':15}  







cbar_ax = fig.add_axes([0.08, 0.59, 0.35, 0.02])
cbar=fig.colorbar(im1, cax=cbar_ax, orientation="horizontal")


""" cbar_ax = fig.add_axes([0.08, 0.24, 0.35, 0.02])
cbar=fig.colorbar(im3, cax=cbar_ax, orientation="horizontal") """

fig.subplots_adjust(bottom=0.25)

# create the colorbar
#np.max
#cb = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm, extend='max', ticks=bounds)
plt.show()



