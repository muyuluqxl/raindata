import numpy as np

# 生成一个3x4x2的三维矩阵
data = np.random.rand(3, 4, 2)
print(data)
# 将三维矩阵展平成一个一维向量
flattened_data = data.flatten()

# 将一维向量重新排列成一个2维矩阵
reshaped_data = flattened_data.reshape(3, 8)

# 打印转换后的矩阵
print(reshaped_data)