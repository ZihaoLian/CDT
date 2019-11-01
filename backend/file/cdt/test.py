import file.cdt.cdt_feature_creator
# import explanation_creator
from file.cdt.explanation_creator import Explanation
import numpy as np
import io
from file.cdt.XGB import XGB


class CDT(object):

    def detect(self, first_path, copy_path, hour, minute):
        cdt_creator=file.cdt.cdt_feature_creator.CdtModel()
        explanation_creator=Explanation()

        # *_clock 都为np.ndarray ,hour,minute为要求的时间，buffer为缓冲
        command_clock=np.loadtxt(open(first_path,"rb"),delimiter=",",skiprows=0)
        copy_clock=np.loadtxt(open(copy_path,"rb"),delimiter=",",skiprows=0)
        hour=3
        minute=25
        buffer=io.BytesIO()

        #返回np.ndarray
        feature=cdt_creator.make_cdt_feature(command_clock,copy_clock,hour,minute,buffer)
        xgb = XGB()
        xgb.train('feature.csv', feature)

# rf=joblib.load('rf.m')
# #如果要换模型需要改explanation_creator.py
# #返回label,支持该分类的解释，不支持该分类的解释 类型为List
# print(explanation_creator.explain(rf,feature))
c = CDT()
c.detect("73471568716181723_1.csv", "73471568716181723_2.csv", 3, 25)












# import cdt_feature_creator
# import explanation_creator
# import numpy as np
# import io
# from sklearn.externals import joblib


# class Singleton(object):
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
#         return cls._instance


# class Clock(Singleton):
#     explanation_creator = explanation_creator.Explanation()
#     rf = joblib.load('rf.m')
#
#     @classmethod
#     def detect(cls, path_origin, path_copy, hour, minute):
#         cdt_creator = cdt_feature_creator.CdtModel()
#         # *_clock 都为np.ndarray ,hour,minute为要求的时间，buffer为缓冲
#         command_clock = np.loadtxt(open(str(path_origin), "rb"), delimiter=",", skiprows=0)
#         copy_clock = np.loadtxt(open(str(path_copy), "rb"), delimiter=",", skiprows=0)
#         hour = hour
#         minute = minute
#         buffer = io.BytesIO()
#
#         # 返回np.ndarray
#         feature = cdt_creator.make_cdt_feature(command_clock, copy_clock, hour, minute, buffer)
#
#         # 如果要换模型需要改explanation_creator.py
#         # 返回label,支持该分类的解释，不支持该分类的解释 类型为List
#         explanation_list = cls.explanation_creator.explain(cls.rf, feature)
#         return explanation_list
#
# myclock = Clock()
# myclock.detect("5d1f1568701304158_1.csv", "5d1f1568701304158_2.csv", 11, 35)