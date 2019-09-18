import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
from cdt_util import count_distance
from cdt_util import get_bounding_box
from cdt_util import merge_multiple_strokes
from cdt_util import get_cloest_distance
from cdt_util import INF

#识别笔画区域，将区域分出数字区域和指针区域
class SvmModel:

    def __init__(self):
        self.model= joblib.load('./svm_train_1_model.m')

    def make_feature(self,strokes,center,indexs,bounding_box,area_indexs,kmeans_label,edge_strokes):
        features=np.zeros((len(area_indexs),13))
        #计算笔画所在区域的包围盒
        area_box=np.zeros((len(area_indexs),5)) #minx,maxx,miny,maxy,label
        #print(edge_indexs)
        #edge_indexs=[i for i,x in enumerate(kmeans_label) if x==1]
        #edge_strokes=merge_multiple_strokes(strokes,strokes_indexs,edge_indexs)
        for i in range(len(area_indexs)):
            area_box[i][0],area_box[i][1]=INF,0
            area_box[i][2],area_box[i][3]=INF,0
            #画出区域内的笔画
            for j in range(len(area_indexs[i])):
                curbox=get_bounding_box(strokes[indexs[area_indexs[i][j], 0]:indexs[area_indexs[i][j], 1],:])
                area_box[i][0]=min(curbox[0],area_box[i][0])
                area_box[i][1]=max(curbox[1],area_box[i][1])
                area_box[i][2]=min(curbox[2],area_box[i][2])
                area_box[i][3]=max(curbox[3],area_box[i][3])
        #print(area_box)
        for i in range(len(area_indexs)):    
            #区域的长度
            features[i,0]=math.fabs(area_box[i][1]-area_box[i][0])
            #区域的宽度
            features[i,1]=math.fabs(area_box[i][3]-area_box[i][2])
            #print("area_size",features[i,0],features[i,1])
            #区域的面积
            features[i,2]=features[i,6]*features[i,7]
            #区域中心与钟表中心的坐标差
            area_center=np.zeros(2)
            area_center[0]=(area_box[i][1]+area_box[i][0])/2
            area_center[1]=(area_box[i][2]+area_box[i][3])/2
            features[i,3]=area_center[0]-center[0]
            features[i,4]=area_center[1]-center[1]
            #区域中心到钟表中心的距离
            features[i,5]=count_distance(area_center[0],area_center[1],center[0],center[1])
            #笔画中心到钟表中心夹角
            features[i,6]=math.degrees(math.atan((area_center[1]-center[1])/(area_center[0]-center[0])))
            if area_center[0]<center[0]:
                features[i,6]+=180
            elif area_center[1]<center[1]:
                features[i,6]+=360
            #if len(area_indexs[i])>0:
                #区域的起始时间
                #features[i,7]=strokes[indexs[area_indexs[i][0]][0],2]
            #笔画长度
            features[i,7]=0
            for j in range(len(area_indexs[i])):
                for k in range(indexs[area_indexs[i][j],0],indexs[area_indexs[i][j],1]-1):
                    features[i,7]+=count_distance(strokes[k,0],strokes[k,1],strokes[k+1,0],strokes[k+1,1])
            features[i,7]=features[i,8]/len(area_indexs[i])
            #笔画长度与区域长度的积
            features[i,8]=features[i,8]*features[i,0]
            #笔画长度与区域宽度的积
            features[i,9]=features[i,8]*features[i,1]
            #笔画到钟表外圈的最近距离
            area_strokes=merge_multiple_strokes(strokes,indexs,area_indexs[i])
            features[i,10]=get_cloest_distance(edge_strokes[:,:2],area_strokes[:,:2])
            #kmeans分类出来的结果作为特征
            stroke_kmeans_label=kmeans_label[area_indexs[i]]
            stroke_kmeans_label_bincount=np.bincount(stroke_kmeans_label)
            features[i,11]=np.argmax(stroke_kmeans_label_bincount)
            features[i,12]=stroke_kmeans_label_bincount[int(features[i,12])]/stroke_kmeans_label.shape[0]
            #label
            #features[i,13]=area_box[i][4]
        cnt=len(area_indexs)
        #归一化，别改这里
        features[:cnt,:11] = StandardScaler().fit_transform(features[:cnt,:11])
        features[:cnt,:11] =MinMaxScaler().fit_transform(features[:cnt,:11])
        return features
        
    def predict_by_data(self,strokes,center,indexs,bounding_box,area_indexs,kmeans_label,edge_strokes):
        feature=self.make_feature(strokes,center,indexs,bounding_box,area_indexs,kmeans_label,edge_strokes)
        return self.model.predict(feature)