import cdt_feature_creator
import explanation_creator
import numpy as np
import io
from sklearn.externals import joblib
cdt_creator = cdt_feature_creator.CdtModel()
explanation_creator = explanation_creator.Explanation()

# *_clock 都为np.ndarray ,hour,minute为要求的时间，buffer为缓冲
command_clock = np.loadtxt(open("opNJ75dEK-K1lAi_k0lH8ZqHiB9I_1_1.csv","rb"),delimiter=",", skiprows=0)
copy_clock = np.loadtxt(open("opNJ75dEK-K1lAi_k0lH8ZqHiB9I_1_2.csv","rb"),delimiter=",", skiprows=0)
hour = 10
minute = 10
buffer = io.BytesIO()


# 返回np.ndarray
feature = cdt_creator.make_cdt_feature(command_clock, copy_clock, hour, minute, buffer)

rf = joblib.load('rf.m')
# 如果要换模型需要改explanation_creator.py
# 返回label,支持该分类的解释，不支持该分类的解释 类型为List
explanation_creator.explain(rf, feature)