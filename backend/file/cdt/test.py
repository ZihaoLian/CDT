import cdt_feature_creator
from explanation_creator import Explanation
import numpy as np
import io
from sklearn.externals import joblib


def test(self):
    print("测试")
    cdt_creator = cdt_feature_creator.CdtModel()
    explanation_creator = Explanation()

    # *_clock 都为np.ndarray ,hour,minute为要求的时间，buffer为缓冲
    command_clock = np.loadtxt(open("20991568653277626_1.csv", "rb"), delimiter=",", skiprows=0)
    copy_clock = np.loadtxt(open("20991568653277626_2.csv", "rb"), delimiter=",", skiprows=0)
    hour = 3
    minute = 25
    buffer = io.BytesIO()

    # 返回np.ndarray
    feature = cdt_creator.make_cdt_feature(command_clock, copy_clock, hour, minute, buffer)
    # xgb = XGB()
    # xgb.train('cdt_feature.csv', feature)

    rf = joblib.load('rf.m')
    # 如果要换模型需要改explanation_creator.py
    # 返回label,支持该分类的解释，不支持该分类的解释 类型为List
    print(explanation_creator.explain(rf, feature))

# class CDT(object):
#     def __init__(self):
#         pass





# import cdt_feature_creator
# import explanation_creator
# import numpy as np
# import io
# from sklearn.externals import joblib
#
#
# class Singleton(object):
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
#         return cls._instance
#
#
# # class Clock(Singleton):
# #     cdt_creator = cdt_feature_creator.CdtModel()
# #     explanation_creator = explanation_creator.Explanation()
# #
# #     @staticmethod
# #     def detect():
# #         # *_clock 都为np.ndarray ,hour,minute为要求的时间，buffer为缓冲
# #         command_clock = np.loadtxt(open("excel.csv", "rb"), delimiter=",", skiprows=0)
# #         copy_clock = np.loadtxt(open("excel2.csv", "rb"), delimiter=",", skiprows=0)
# #         hour = 5
# #         minute = 40
# #         buffer = io.BytesIO()
# #
# #         # 返回np.ndarray
# #         feature = cdt_creator.make_cdt_feature(command_clock, copy_clock, hour, minute, buffer)
# #
# #         rf = joblib.load('rf.m')
# #         # 如果要换模型需要改explanation_creator.py
# #         # 返回label,支持该分类的解释，不支持该分类的解释 类型为List
# #         explanation_list = explanation_creator.explain(rf, feature)
# #         return explanation_list
#
