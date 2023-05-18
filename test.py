from scipy.io import loadmat
import numpy as np
import csv
import scipy.io as scio
import matplotlib.pyplot as plt
import scipy.stats as stats

class WData:
    def __init__(self,wdata_path) -> None:
        self.data = loadmat(wdata_path)
    
    @property
    def lat(self):
        return self.data['Lat'][0]
    
    @property
    def lon(self):
        return self.data['Lon'][0]
    
    @property
    def stanum(self):
        return self.data['Stanum'][0]
    
    @property
    def lat_lon(self):
        return np.stack([self.data['Lat'][0],self.data['Lon'][0]],axis=-1)
    
    def get(self,year,month,day):
        if not isinstance(year,int) or not isinstance(month,int) or not isinstance(day,int):
            raise ValueError('params must be int')
        if year < 1961 or year >= 2022:
            raise ValueError('year must between 1961 - 2022')
        if month < 6 or month > 8:
            raise ValueError('month must between 6 - 8')
        if day <= 0 or day > 30:
            raise ValueError('day must between 1 - 30')
        year_idx = year - 1961
        month_idx = f'pre_{str(month).zfill(2)}'
        return np.nan_to_num(self.data[month_idx][:,year_idx,:][:,day],nan=0)


Path='PRE_1961_2022_summer.mat'
data = scio.loadmat("PRE_1961_2022_summer.mat")

wdata = WData(Path)
Stanum = wdata.stanum
Lat = wdata.lat
Lon = wdata.lon

mouth=['pre_06']
for mouth_idx in mouth:
    pre = data[mouth_idx]
    #print(mouth_idx)
    #print(pre.shape)
    x,y,z = pre.shape
    pre = np.nan_to_num(pre)
    pre_mean_mouth = np.nanmean(pre, axis = 2)
    pre_var_mouth = np.around(np.nanvar(pre, axis = 2),2)
    pre_mean_all = np.nanmean(pre_mean_mouth, axis = 1).reshape(699,1)
    pre_mean_mouth = np.nan_to_num(pre_mean_mouth)
    pre_mean_all = np.nan_to_num(pre_mean_all)
    all_rainpct=np.around(((pre_mean_mouth-pre_mean_all)/pre_mean_all)* 100,decimals=2)

    for year_idx in range(1):
        cavout='./contrastCsv/test.txt'\
        .format(year=1961+year_idx,mouth=mouth_idx)
        print(cavout)
        rainpct=all_rainpct[:,year_idx]
        pre_mean_mouth=np.around(pre_mean_mouth,2)
        mean=pre_mean_mouth[:,year_idx]
        var=pre_var_mouth[:,year_idx]
        with open(cavout, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['Stanum', 'Lat', 'Lon', 'Rain','Mean','Var'])
            for i in range(699):
                writer.writerow([Stanum[i], Lat[i], Lon[i] ,rainpct[i],mean[i],var[i]]) 
