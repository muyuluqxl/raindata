from scipy.io import loadmat
import numpy as np
import csv

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

with open('./rain_1961_6_1.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['Stanum', 'Lat', 'Lon', 'Rain'])
    for i in range(699):
         writer.writerow([Stanum[i], Lat[i]/100, Lon[i]/100 ,Rain[i]])


""" 
data = loadmat(Path)
Stanum=data["Stanum"].reshape(699,)
Lat=data["Lat"].reshape(699,)
Lon=data["Lon"].reshape(699,)
rain_data=WData(Path).get(1961,6,1) """