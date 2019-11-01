import numpy as np
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from file.cdt.cdt_util import count_distance

#初步对笔画进行分类，主要是识别出外圈笔画
class KmeansModel:

    def __init__(self):
        self.model= joblib.load('file/cdt/kmeans.model')

    def make_feature(self,strokes,center,indexs,bounding_box):
        cnt=indexs.shape[0]
        features=np.zeros((cnt,4))
        for i in range(cnt):
            #笔画起始时间
            features[i,0]=strokes[indexs[i][0],2]
            #笔画中心到钟表中心的距离
            features[i,1]=count_distance((bounding_box[i][1]+bounding_box[i][0])/2,(bounding_box[i][3]+bounding_box[i][2])/2,center[0],center[1])
            #第一点到中心的距离
            features[i,2]=count_distance(strokes[indexs[i][0]][0],strokes[indexs[i][0]][1],center[0],center[1])
            #最后一点到中心的距离
            features[i,3]=count_distance(strokes[indexs[i][1]-1][0],strokes[indexs[i][1]-1][1],center[0],center[1])
        #归一化，别改这里
        features[:cnt,:4] = StandardScaler().fit_transform(features[:cnt,:4])
        features[:cnt,:4] =MinMaxScaler().fit_transform(features[:cnt,:4])
        return features
        
    def predict_by_data(self,strokes,center,indexs,bounding_box):
        feature=self.make_feature(strokes,center,indexs,bounding_box)
        return self.model.predict(feature)