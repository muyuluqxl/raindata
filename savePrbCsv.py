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
wdata = WData(Path)
Stanum = wdata.stanum
Lat = wdata.lat
Lon = wdata.lon
Rain = wdata.get(1961,6,1) 

Path='PRE_1961_2022_summer.mat'
data = scio.loadmat("PRE_1961_2022_summer.mat")

wdata = WData(Path)
Stanum = wdata.stanum
Lat = wdata.lat
Lon = wdata.lon

mouth=['pre_06','pre_07','pre_08']
for mouth_idx in mouth:
    allStan_allYear = data[mouth_idx]
    allStan_allYear = np.nan_to_num(allStan_allYear)
    for year_idx in range(62):
        allStan_oneYear = allStan_allYear[:,year_idx,:]
        pre=[]
        for stan_idx in range(699):            
            #所有数据fit
            oneStan_allYear = allStan_allYear[stan_idx]
            fitdata = np.nan_to_num(oneStan_allYear).reshape(-1,1)
            chi2 = stats.chi2
            df,loc,scale = chi2.fit(fitdata,floc=0)
            #期望计算概率值
            oneStan_oneYear = allStan_oneYear[stan_idx]
            ex = np.mean(oneStan_oneYear)
            pdf=chi2.pdf(ex,df,loc,scale)
            pdf=0.0 if(pdf< 1e-99) or (pdf >100) else pdf
            pre.append(round(pdf*100,2))
            #print(ex,pdf)
        cavout='./PrbCsv/prbrain_{year}_{mouth}.csv'\
        .format(year=1961+year_idx,mouth=mouth_idx)
        print(cavout)
        rainprb=pre
        with open(cavout, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['Stanum', 'Lat', 'Lon', 'Rain'])
            for i in range(699):
                writer.writerow([Stanum[i], Lat[i], Lon[i] ,rainprb[i]]) 

""" mouth=['pre_06','pre_07','pre_08']
for mouth_idx in mouth:
    pre = data[mouth_idx]
    print(mouth_idx)
    print(pre.shape)
    x,y,z = pre.shape
    pre_mean_mouth = np.nanmean(pre, axis = 2)
    #print(pre_mean_mouth.shape)
    pre_mean_all = np.nanmean(pre_mean_mouth, axis = 1).reshape(699,1)
    pre_mean_mouth = np.nan_to_num(pre_mean_mouth)
    pre_mean_all = np.nan_to_num(pre_mean_all)
    all_rainpct=((pre_mean_mouth-pre_mean_all)/pre_mean_all)* 100
    #print(all_rainpct.shape) """

""" pre = np.nan_to_num(data['pre_06'][0][0]).reshape(-1,1)
Y=pre
chi2 = stats.chi2
df,loc,scale = chi2.fit(Y,floc=0)
x = np.linspace(-1,20,100)
#pdf_fitted = gamma.pdf(x, fit_alpha, fit_loc, fit_beta)
result = chi2.expect(lambda x: x, args=(df,), loc=loc, scale=scale)
print(result) """
