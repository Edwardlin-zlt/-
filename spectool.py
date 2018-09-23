#!usr/bin/env python

"""
为了处理光谱信息开发的小程序

Author: Edward
Email: Edwardlin.zlt@gmail.com
"""

# import modules----------------------------------------
import re
import os
from collections import OrderedDict

import pandas as pd

from keys import keys
# import modules down-------------------------------------

class Spectrum(object):
    """
    导入仪器数据，将其数据定义成一个光谱对象，主要属性有`data`和`spec_dict`
    """
    

    def __init__(self,filepath):
        """
        ::filepath (str): 仪器文件路径
        ::self.__data (dict): 包含亮度，色度坐标等信息的字典
        ::self.__spec_dict: SPD数据，默认为380-780之间的数据
        """
        self.__data, self.spec_dict = get_spec(filepath)
    
    def get(self, attr):
        return self.__data.get(attr,0)
    
    def __str__(self):
        return str(self.__data)


def get_spec(filepath, start=380, end=780):
    """
    将仪器导出的数据转换成纯粹的光谱数据
    :filepath (str)
    :start(int) 开始的波长
    :end (int) 结束的波长取值
    :re (tuple of spec_data_info and 光谱能量分布) 光谱信息和380-780之间的光谱能量分布
    """
    former = r'(.*data=")([,\.\dE-]*)(".*mfp=")(.*)(" \/>)'

    with open(filepath) as f:
        raw_data = f.read() 
        matched = re.match(former, raw_data)
        data = list(map(float,matched.group(2).split(',')))
        data = dict(zip(keys, data))

        raw_spec = list(zip(range(350, 1001),map(float,matched.group(4).split(','))))
        for x in raw_spec:
            if x[0] == start:
                start_index = raw_spec.index(x)
            elif x[0] == end:
                end_index = raw_spec.index(x)
        spec_dict= OrderedDict(raw_spec[start_index:end_index+1])
        return (data, spec_dict) 

def sps_to_one_csv(dirpath):
    """
    将一个文件夹内所有的光谱文件信息放在一个表格里
    :: dirpath(str): 目标文件夹
    :: re(None): 在当前目录导出一个csv文件
    """
    columns = keys.copy()
    columns.insert(0, 'name')
    df = pd.DataFrame(None, columns= columns)
    i = 0
    files = [x for x in os.listdir(dirpath) if os.path.splitext(x)[1] == '.sp']
    print(files)
    for f in files:
        print("i: ", i)
        print("f: ", f)
        temp_spec = Spectrum(os.path.join(dirpath,f))
        incre_info = [temp_spec.get(x) for x in keys]
        incre_info.insert(0, f.split('_')[0])
        print(list(zip(columns, incre_info)))
        df.loc[i] = incre_info
        i += 1
    df.to_csv(os.path.join(dirpath, 'all.csv'))

dirname = './spectral'
sps_to_one_csv(dirname)
