from sklearn.preprocessing import StandardScaler
import numpy as np

# 生成一个示例数据集
data = np.array([1, 2, 3, 4, 5])
data = data.reshape(-1, 1)
x = [[10, 20],
        [15, 25],
        [20, 30],
        [25, 35]]
print(data.shape)
print(len(x))
# 创建StandardScaler对象并拟合数据
scaler = StandardScaler().fit(data)

# 对数据进行标准化
scaled_data = scaler.transform(data)

# 打印标准化后的数据
print(scaled_data)
