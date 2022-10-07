import numpy as np
import pandas as pd

# 1. 读取数据
data = pd.read_excel('C:\\Users\\Administrator\\Desktop\\数据.xlsx')
# 保存数据
data.to_excel('C:\\Users\\Administrator\\Desktop\\数据.xlsx')

# 2. 读取列
# 此处双中括号读取出的形式就是dataframe
stock_code = data[['股票代码', '一']]
# 单中括号读取出的就是Series
stock_code = data['股票代码']
# 读取到的数据可以使用np.array()转成ndarray的数组格式
np.array(stock_code)
'''
dataframe和series区别：
series，只是一个一维数据结构，它由index和value组成。
dataframe，是一个二维结构，除了拥有index和value之外，还拥有column。
联系：
dataframe由多个series组成，无论是行还是列，单独拆分出来都是一个series。
一般还是dataframe用的多
'''

# 3. 读取行
# dataframe读取行 固定用法
read_line = data[0:3]
read_line = data.loc[3]

# 4. 删除空行
data = data.dropna()
# dropna之后的索引并不会改变，可能是1 13 14 15
# 所以需要充值索引
data.reset_index(drop=True, inplace=True)


# 5. 为某一列赋值
data.loc[5] = [stock_code.loc[5, '股票代码'], 0]

