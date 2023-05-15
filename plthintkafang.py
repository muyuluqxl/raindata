import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2

# 生成随机数据
data = np.random.randn(1000)

# 绘制统计概率直方图
n, bins, patches = plt.hist(data, bins=30, density=True, alpha=0.5)

# 计算卡方分布的概率密度函数
df,loc,scale = chi2.fit(data)
x = np.linspace(chi2.ppf(0.01, df), chi2.ppf(0.99, df), 1000)
y = chi2.pdf(x,df,loc,scale)


# 添加标题和轴标签
plt.title('Probability Histogram and Chi-Square Fit')
plt.xlabel('Value')
plt.ylabel('Probability Density')

# 显示图形
plt.show()