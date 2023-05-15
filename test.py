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


Path='E:/code/python/gis/frykit/frykit/data/PRE_1961_2022_summer.mat'
wdata = WData(Path)
Stanum = wdata.stanum
Lat = wdata.lat
Lon = wdata.lon
Rain = wdata.get(1961,6,1) 

Path='E:/code/python/gis/frykit/frykit/data/PRE_1961_2022_summer.mat'
data = scio.loadmat("E:/code/python/gis/frykit/frykit/data/PRE_1961_2022_summer.mat")

wdata = WData(Path)
Stanum = wdata.stanum
Lat = wdata.lat
Lon = wdata.lon

mouth=['pre_06']
for mouth_idx in mouth:
    allStan_allYear = data[mouth_idx]
    allStan_allYear = np.nan_to_num(allStan_allYear)
    for year_idx in range(1):
        allStan_oneYear = allStan_allYear[:,year_idx,:]
        pre=[]
        for stan_idx in range(1):
            #所有数据fit
            oneStan_allYear = allStan_allYear[stan_idx]
            fitdata = np.nan_to_num(oneStan_allYear).reshape(-1,1)
            print(fitdata.shape)
            chi2 = stats.chi2
            df,loc,scale = chi2.fit(fitdata,floc=0)
            #期望计算概率值
            oneStan_oneYear = allStan_oneYear[stan_idx]
            ex = np.mean(oneStan_oneYear)
            print(ex)
            pdf=chi2.pdf(ex,df,loc,scale)
            pdf=0.0 if(pdf< 1e-99) or (pdf >100) else pdf
            pre.append(round(pdf*100,2))

"""     pre = data[mouth_idx]
    pre = np.nan_to_num(pre)
    pre_mean_mouth = np.nanmean(pre, axis = 2)
    pre_mean_all = np.nanmean(pre_mean_mouth, axis = 1)
    pre_mean_all = np.nan_to_num(pre_mean_all)
    #

    allStan_allYear = data[mouth_idx]
    for year_idx in range(1):
        allStan_oneYear = allStan_allYear[:,year_idx,:]
        pre=[]
        for stan_idx in range(1):            
            oneStan_oneYear = allStan_oneYear[stan_idx]
            oneStan_oneYear = np.nan_to_num(oneStan_oneYear)
            print(oneStan_oneYear.shape)
            #chi2 = stats.chi2
            #df,loc,scale = chi2.fit(Y,floc=0) """