'''
@Description: In User Settings Edit
@Author: your name
@Date: 2019-09-16 00:08:50
@LastEditTime: 2019-09-16 01:12:42
@LastEditors: Please set LastEditors
'''
import cdt_feature_creator
import explanation_creator
import numpy as np
import io
from sklearn.externals import joblib
cdt_creator = cdt_feature_creator.CdtModel()
explanation_creator = explanation_creator.Explanation()

# *_clock 都为np.ndarray ,hour,minute为要求的时间，buffer为缓冲
command_clock = np.loadtxt(open("excel.csv", "rb"), delimiter=",", skiprows=0)
copy_clock = np.loadtxt(
    open("excel2.csv", "rb"), delimiter=",", skiprows=0)
hour = 5
minute = 40
buffer = io.BytesIO()


# 返回np.ndarray
feature = cdt_creator.make_cdt_feature(
    command_clock, copy_clock, hour, minute, buffer)

rf = joblib.load('rf.m')
# 如果要换模型需要改explanation_creator.py
# 返回label,支持该分类的解释，不支持该分类的解释 类型为List
explanation_creator.explain(rf, feature)
