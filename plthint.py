import numpy as np
import matplotlib.pyplot as plt
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


allStan_allYear = data['pre_06']
allStan_allYear = np.nan_to_num(allStan_allYear)

oneStan_allYear = allStan_allYear[0]
Y = np.nan_to_num(oneStan_allYear).reshape(-1,1)
dataY=Y 

""" allStan_allYear = data['pre_06']
allStan_allYear = np.nan_to_num(allStan_allYear)
pre_mean_mouth = np.mean(allStan_allYear,axis=2)

oneStan_allYear = allStan_allYear[0]
Y = np.nan_to_num(oneStan_allYear).reshape(-1,1)
dataY=Y  """

# 计算数据的概率密度函数
n, bins, patches = plt.hist(dataY, bins=30, density=True, alpha=0.5)

chi2 = stats.chi2
df,loc,scale = chi2.fit(Y,floc=0)
x = np.linspace(chi2.ppf(0.01, df), chi2.ppf(0.99, df), 1000)
plt.plot(x,chi2.pdf(x,df,loc,scale))
# 绘制概率密度函数曲线

# 添加图标题和轴标签
plt.title('Probability Histogram')
plt.xlabel('Value')
plt.ylabel('Probability Density')

# 显示图形
plt.show()