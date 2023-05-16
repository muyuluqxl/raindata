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

wdata = WData(Path)
Stanum = wdata.stanum
Lat = wdata.lat
Lon = wdata.lon

for mouth_idx in ['pre_06','pre_07','pre_08']:
    AnoData = np.zeros((62,699),dtype=np.float16)
    for year_idx in range(62):
        Anoread='./rainCsv/rain_{year}_{mouth}.csv'\
        .format(year=1961+year_idx,mouth=mouth_idx)
        AnoFile = pd.read_csv(Anoread,header=0)
        AnoFile['Rain']=AnoFile['Rain'].abs()
        for stan_idx in range(699): 
            AnoData[year_idx][stan_idx]=AnoFile['Rain'][stan_idx]
    scaler = StandardScaler().fit(AnoData)
    scaled_data = scaler.transform(AnoData)
    scaled_data = np.round(scaled_data, 2)
    for year_idx in range(62):
        cavout='./standAnoCsv/Ano_{year}_{mouth}.csv'\
        .format(year=1961+year_idx,mouth=mouth_idx)
        with open(cavout, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['Stanum', 'Lat', 'Lon', 'Rain'])
            rainpct=scaled_data[year_idx]
            for i in range(699):
                writer.writerow([Stanum[i], Lat[i], Lon[i] ,rainpct[i]]) 
