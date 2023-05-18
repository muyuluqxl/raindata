import csv
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from scipy.io import loadmat
import numpy as np
import csv
import scipy.io as scio

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

mouth=['pre_06','pre_07','pre_08']
for mouth_idx in mouth:
    pre = data[mouth_idx]
    pre = np.nan_to_num(pre)
    for stan_idx in range(699):
        write='./stanvalueCsv/{stan}_{lat}′N{lon}′E_{mouth}.csv'\
            .format(stan=Stanum[stan_idx],lat=round(Lat[stan_idx]/100,2),lon=round(Lon[stan_idx]/100,2),mouth=mouth_idx)
        year = list(range(1961,2023))
        with open(write,'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(year)
            transposed_matrix = zip(*pre[stan_idx])
            for row in transposed_matrix:
                writer.writerow(row)