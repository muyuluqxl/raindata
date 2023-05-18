import pandas as pd
import os
csv_files = [f for f in os.listdir('./PrbCsv') if f.endswith('.csv')]
# 删除每个 CSV 文件的最后三行数据
for file in csv_files:
    filename = './PrbCsv/'+file
    print(filename)
    # 读取 CSV 文件
    df = pd.read_csv(filename)

