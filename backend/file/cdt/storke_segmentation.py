import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
from cdt_util import count_distance
from cdt_util import get_cloest_distance

#将构成同一元素的笔画分成一个区域
class AdaboostModel:

    def __init__(self):
        self.model= joblib.load('./train1_model.m')

    #生成特征
    def make_feature(self,strokes,center,indexs,bounding_box):
        #判断相交或重叠的最小距离
        min_distance=5
        cnt=indexs.shape[0]
        features=np.zeros((cnt,17),dtype=np.float64)
    #print(helper)
    #print(center)
    #根据规则生成特征
        for i in range(cnt-1):
            #单笔画特征
            #笔画开始时间
            features[i,0]=abs(strokes[indexs[i+1,0],2])
            #笔画宽度
            features[i,1]=abs(bounding_box[i,1]-bounding_box[i,0])
            #笔画高度
            features[i,2]=abs(bounding_box[i,2]-bounding_box[i,3])
            #笔画长度
            features[i,3]=0
            for j in range(indexs[i,0],indexs[i,1]-1):
                features[i,3]+=count_distance(strokes[j,0],strokes[j,1],strokes[j+1,0],strokes[j+1,1])
            #第一点到中心距离
            features[i,4]=count_distance(strokes[indexs[i,0]][0],strokes[indexs[i,0]][1],center[0],center[1])
            #时间意义上的中间一点到中心距离
            mid=(int)((indexs[i,0]+indexs[i,1])/2)
            features[i,5]=count_distance(strokes[mid,0],strokes[mid,1],center[0],center[1])
            #最后一点到中心距离
            features[i,6]=count_distance(strokes[indexs[i,1]-1][0],strokes[indexs[i,1]-1][1],center[0],center[1])
            #以中心为顶点与x轴夹角
            features[i,7]=math.atan(abs((bounding_box[i,3]+bounding_box[i,2])/2-center[1])/abs((bounding_box[i,1]+bounding_box[i,0])/2-center[0]))                          
            
            
            #笔画间特征
            #时间差
            features[i,8]=abs(strokes[indexs[i+1,0],2]-strokes[indexs[i,0],2])
            #以中心为顶点与两笔画中心的夹角
            features[i,9]=math.atan(abs((bounding_box[i,3]+bounding_box[i,2])/2-center[1])/abs((bounding_box[i,1]+bounding_box[i,0])/2-center[0]))-math.atan(abs((bounding_box[i+1,3]+bounding_box[i+1,2])/2-center[1])/abs((bounding_box[i+1][1]+bounding_box[i+1][0])/2-center[0]))
            #和下一笔之间的开始距离
            features[i,10]=count_distance(strokes[indexs[i,0]][0],strokes[indexs[i,0]][1],strokes[indexs[i+1,0]][0],strokes[indexs[i+1,0]][1])
            #和下一笔之间时间中间一点的距离
            next_mid=(int)((indexs[i+1,0]+indexs[i+1,1])/2)
            features[i,11]=count_distance(strokes[mid,0],strokes[mid,1],strokes[next_mid,0],strokes[next_mid,1])
            #和下一笔之间的结束距离
            features[i,12]=count_distance(strokes[indexs[i,1]-1][0],strokes[indexs[i,1]-1][1],strokes[indexs[i+1,1]-1][0],strokes[indexs[i+1,1]-1][1])
            #和下一笔之间的中心距离
            features[i,13]=count_distance((bounding_box[i,1]+bounding_box[i,0])/2,(bounding_box[i,3]+bounding_box[i,2])/2,(bounding_box[i+1,1]+bounding_box[i+1,0])/2,(bounding_box[i+1,3]+bounding_box[i+1,2])/2)
            #与下一笔的最短距离
            features[i,14]=get_cloest_distance(strokes[indexs[i,0]:indexs[i,1],:2],strokes[indexs[i+1,0]:indexs[i+1,1],:2])
            #和下一笔之间的结束开始距离
            features[i,15]=count_distance(strokes[indexs[i,1]-1][0],strokes[indexs[i,1]-1][1],strokes[indexs[i+1,0]][0],strokes[indexs[i+1,0]][1])
            #是否与下一笔连接
            last_distance=get_cloest_distance(strokes[indexs[i,0]:indexs[i,1],:],strokes[indexs[i+1,0]:indexs[i+1,1],:])
            #last_distance=count_distance(strokes[indexs[i,1]-1][0],strokes[indexs[i,1]-1][1],strokes[indexs[i+1,0]][0],strokes[indexs[i+1,0]][0])                 
            if(last_distance<=min_distance):
                features[i,16]=1
            else:
                features[i,16]=0                                            
        #归一化
        features[:cnt-1,:16] = StandardScaler().fit_transform(features[:cnt-1,:16])
        features[:cnt-1,:16] =MinMaxScaler().fit_transform(features[:cnt-1,:16])
        return features[:cnt-1,:]
        
    def predict_by_data(self,strokes,center,indexs,bounding_box):
        feature=self.make_feature(strokes,center,indexs,bounding_box)
        return self.model.predict(feature)