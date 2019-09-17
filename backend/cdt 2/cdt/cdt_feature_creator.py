import os
import cv2
import math
import numpy as np
import itertools
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.utils.extmath import softmax
from sklearn.preprocessing import normalize

import hand
import digit_classification
import stroke_classification
import storke_segmentation
import area_classification

#from cdt_util import *
from cdt_util import count_center
from cdt_util import get_strokes_index
from cdt_util import get_bounding_box
from cdt_util import merge_multiple_strokes
from cdt_util import count_stroke_length
from cdt_util import get_cloest_distance
from cdt_util import get_polar_coordinates
from cdt_util import get_real_child
from cdt_util import INF
from cdt_util import count_distance
from cdt_util import dcmp
from cdt_util import overlap
class CdtModel:
    def __init__(self):
        #钟表每个数字的个数，例如 0：1个 ，1：5个
        self.digit_size=[1,5,2,1,1,1,1,1,1,1]
        #钟表每个数字对应的标准角度
        self.digit_angles=[[150],[60,90,120,120,150],[30,90],[0],[330],[300],[270],[240],[210],[180]]
        #初步识别出钟表外圈
        self.kmeans_model=stroke_classification.KmeansModel()
        #将笔画分为区域
        self.adaboost_model=storke_segmentation.AdaboostModel()
        #将笔画区域识别出数字区域和指针区域
        self.svm_model=area_classification.SvmModel()
        #数字识别
        self.digit_detector=digit_classification.DigitDetector()
        #指针识别
        self.hand_detector = hand.HandDetect()
    def make_cdt_feature(self,command_strokes,copy_strokes,hour,minute,buffer):
        cnt=200
        cdt_feature=np.zeros(408)
        cdt_feature[:cnt],command_digit_num=self.make_single_clock_feature(command_strokes,hour,minute,buffer)
        cdt_feature[cnt:2*cnt],copy_digit_num=self.make_single_clock_feature(copy_strokes,hour,minute,buffer)
        #重复数字数
        cdt_feature[2*cnt]=cdt_feature[170]+cdt_feature[cnt+170]
        #缺失数字数
        cdt_feature[2*cnt+1]=cdt_feature[171]+cdt_feature[cnt+171]
        #数字平均长度
        cdt_feature[2*cnt+2]=(cdt_feature[173]*command_digit_num+cdt_feature[cnt+173]*copy_digit_num)/(command_digit_num+copy_digit_num)
        #数字平均高度
        cdt_feature[2*cnt+3]=(cdt_feature[176]*command_digit_num+cdt_feature[cnt+176]*copy_digit_num)/(command_digit_num+copy_digit_num)
        #数字平均宽度
        cdt_feature[2*cnt+4]=(cdt_feature[177]*command_digit_num+cdt_feature[cnt+177]*copy_digit_num)/(command_digit_num+copy_digit_num)
        #总笔画数
        cdt_feature[2*cnt+5]=cdt_feature[193]+cdt_feature[cnt+193]
        #整个实验的时间
        cdt_feature[2*cnt+6]=cdt_feature[197]+cdt_feature[cnt+197]
        #思考时间与总时间的比值
        cdt_feature[2*cnt+7]=math.fabs(cdt_feature[197]-cdt_feature[195])+math.fabs(cdt_feature[cnt+197]-cdt_feature[cnt+195])/cdt_feature[2*cnt+6]
        return cdt_feature
    def make_single_clock_feature(self,strokes,hour,minute,buffer):           
        #strokes=np.loadtxt(open(os.path.join(root, name),"rb"),delimiter=",",skiprows=0)
        center=count_center(strokes)
        strokes_indexs=get_strokes_index(strokes)
        bounding_box=np.zeros((strokes_indexs.shape[0],6))
        #print(strokes_indexs)
        for i in range(strokes_indexs.shape[0]):
            bounding_box[i]=get_bounding_box(strokes[strokes_indexs[i,0]:strokes_indexs[i,1],:])
        #从笔画中分类出外圈笔画
        kmeans_label=self.kmeans_model.predict_by_data(strokes,center,strokes_indexs,bounding_box)
        #用椭圆拟合外圈，要求最少含五个不重复的点
        edge_indexs=[i for i,x in enumerate(kmeans_label) if x==1]
        edge_strokes=merge_multiple_strokes(strokes,strokes_indexs,edge_indexs)
        clean_edge_strokes=edge_strokes[np.where(edge_strokes[:,0]>=0)]
        if clean_edge_strokes.shape[0]>=5:
            int_edge_strokes=np.array([[int(i[0]),int(i[1])] for i in clean_edge_strokes])
            edge_ellipse=cv2.fitEllipse(int_edge_strokes)#椭圆 （（中心x,y），（长轴，短轴），旋转角） #要判断
            center=edge_ellipse[0]
        
        internal_indexs=strokes_indexs[kmeans_label!=1]
        #将构成同一元素的笔画分成同一区域
        adaboost_label=self.adaboost_model.predict_by_data(strokes,center,internal_indexs,bounding_box)
        area_indexs=self.get_areas_indexs(strokes,internal_indexs,adaboost_label)
        
        #将区域分出数字区域和指针区域
        svm_label=self.svm_model.predict_by_data(strokes,center,internal_indexs,bounding_box,area_indexs,kmeans_label,edge_strokes)

        digit_temp_list=[i for i,x in enumerate(svm_label.tolist()) if x==2]
        digit_area_indexs=[y for j,y in enumerate(area_indexs) if j in digit_temp_list]
        hand_area_indexs=[y for j,y in enumerate(area_indexs) if j not in digit_temp_list]
        digit_feature=np.zeros((len(digit_area_indexs),25))
        for i in range(len(digit_area_indexs)):
            digit_strokes=merge_multiple_strokes(strokes,internal_indexs,digit_area_indexs[i])
            digit_feature[i,:24]=self.digit_detector.make_feature(digit_strokes)
            digit_feature[i,24]=digit_strokes[-1,1]
        digit_label=self.digit_detector.predict_by_feature(digit_feature[:,:25])

        #合并区域使得补足划分不足的部分
        for i in range(3):
            digit_area_indexs,digit_label=self.repair_under_split(strokes,internal_indexs,digit_area_indexs,digit_label,center)
            #print(digit_area_indexs,digit_label)
            digit_area_indexs,digit_label=self.repair_over_split(strokes,internal_indexs,digit_area_indexs,digit_label,center)
            #print(digit_area_indexs,digit_label)

        digit_info=self.digit_label_to_list(strokes,internal_indexs,digit_area_indexs,digit_label,center)      
        #所有区域按照对应的数字及其极坐标角度theta排序
        for i in range(len(digit_info)):
            digit_info[i]=sorted(digit_info[i],key=(lambda x:x[3]))
        digit_size_difference=self.get_digit_status(digit_info,self.digit_size)[0]
        #处理多余数字
        digit_info=self.choose_clock_digit(digit_info,self.digit_angles,self.digit_size,digit_area_indexs,digit_label)[0]            
        temp_digit_angles=self.digit_angles.copy()
        
        #self.draw_result_picture(strokes,strokes_indexs,kmeans_label,svm_label,digit_label,digit_area_indexs,hand_area_indexs,"")
        
        clock_feature=np.zeros(200)
        cnt=0
        #数字特征
        tol_digit_num,tol_digit_strokes_num,tol_digit_height,tol_digit_width,tol_digit_area_size,tol_digit_length,tol_digit_time=0,0,0,0,0,0,0
        for i in range(len(digit_info)):
            tol_digit_num+=len(digit_info[i])
            for j in range(len(digit_info[i])):
                digit_strokes=merge_multiple_strokes(strokes,internal_indexs,digit_area_indexs[digit_info[i][j][0]])
                minx,maxx,miny,maxy,mint,maxt=get_bounding_box(digit_strokes[np.where(digit_strokes[:,0]>=0)])
                #笔画数
                clock_feature[cnt+j*10+0]=len(digit_area_indexs[digit_info[i][j][0]])
                tol_digit_strokes_num+=clock_feature[cnt+j*10+0]
                #笔画长度
                clock_feature[cnt+j*10+1]=count_stroke_length(digit_strokes)
                tol_digit_length+=clock_feature[cnt+j*10+1]
                #笔画时间
                clock_feature[cnt+j*10+2]=maxt-mint
                tol_digit_time+=clock_feature[cnt+j*10+2]
                #绘画速度
                clock_feature[cnt+j*10+3]=clock_feature[cnt+j*10+1]/clock_feature[cnt+j*10+2]
                #包围盒高度
                clock_feature[cnt+j*10+4]=maxx-minx
                tol_digit_height+=clock_feature[cnt+j*10+4]
                #包围盒宽度
                clock_feature[cnt+j*10+5]=maxy-miny
                tol_digit_width+=clock_feature[cnt+j*10+5]
                #包围盒面积
                clock_feature[cnt+j*10+6]=clock_feature[cnt+j*10+4]*clock_feature[cnt+j*10+5]
                tol_digit_area_size+=clock_feature[cnt+j*10+6]
                #数字中心到钟表中心的距离
                clock_feature[cnt+j*10+7]=digit_info[i][j][2]
                #数字到钟表外圈的最近距离
                clock_feature[cnt+j*10+8]=get_cloest_distance(edge_strokes[:,:2],digit_strokes[:,:2])
                #数字到正确位置的角度差
                difference_angles=[math.fabs(digit_info[i][j][3]-x) for x in temp_digit_angles[i]]
                clock_feature[cnt+j*10+9]=min(difference_angles)
                temp_digit_angles[i][difference_angles.index(clock_feature[cnt+j*10+9])]=-361            
            cnt+=self.digit_size[i]*10
        #print("数字重复或缺失数字cnt",cnt)
        repeat_digit_num,miss_digit_num=0,0
        for i in range(len(digit_size_difference)):
            #数字i重复个数
            if digit_size_difference[i]<0:
                clock_feature[cnt]-=digit_size_difference[i]
                repeat_digit_num+=clock_feature[cnt]
            cnt+=1
            #数字i缺少的个数
            if digit_size_difference[i]>0:
                clock_feature[cnt]+=digit_size_difference[i]
                miss_digit_num+=clock_feature[cnt]
            cnt+=1
        #数字重复总个数
        clock_feature[cnt]=repeat_digit_num
        #print("repet cnt",cnt)
        cnt+=1
        #数字缺失总个数
        clock_feature[cnt]=miss_digit_num
        #print("miss cnt",cnt)
        cnt+=1                
        #数字平均笔画数
        clock_feature[cnt]=tol_digit_strokes_num/tol_digit_num
        cnt+=1
        #数字平均长度
        clock_feature[cnt]=tol_digit_length/tol_digit_num
        #print("length cnt",cnt)
        cnt+=1
        #数字平均绘画时间
        clock_feature[cnt]=tol_digit_time/tol_digit_num
        cnt+=1
        #数字总体绘画速度
        clock_feature[cnt]=tol_digit_length/tol_digit_time
        cnt+=1
        #数字平均高度
        clock_feature[cnt]=tol_digit_height/tol_digit_num
        #print("height cnt",cnt)
        cnt+=1
        #数字平均宽度
        clock_feature[cnt]=tol_digit_width/tol_digit_num
        #print("weight cnt",cnt)
        cnt+=1
        #数字包围盒平均面积
        clock_feature[cnt]=tol_digit_area_size/tol_digit_num
        cnt+=1
        #数字12,3，6，9,是否先画
        temp_pre_list=digit_label[:6,0].tolist()
        temp_pre_list=temp_pre_list[:6]
        pre_draw_list=[1,2,3,6,9]
        if (pre_draw_list>temp_pre_list)-(pre_draw_list<temp_pre_list):
            clock_feature[cnt]=1
        cnt+=1

        #钟表外圈特征
        
        #钟表外圈笔画数
        clock_feature[cnt]=len(edge_indexs)
        cnt+=1
        if len(edge_indexs)>0:
            #钟表外圈笔画长度
            clock_feature[cnt]=count_stroke_length(edge_strokes)
            cnt+=1  
            #钟表外圈笔画时间
            edge_minx,edge_maxx,edge_miny,edge_maxy,edge_mint,edge_maxt=get_bounding_box(clean_edge_strokes)
            clock_feature[cnt]=edge_maxt-edge_mint
            cnt+=1  
            #钟表外圈绘画速度
            clock_feature[cnt]=clock_feature[cnt-2]/clock_feature[cnt-1]
            cnt+=1  
            #钟表外圈拟合椭圆的长轴
            clock_feature[cnt]=edge_ellipse[1][0]
            cnt+=1  
            #钟表外圈拟合椭圆的短轴
            clock_feature[cnt]=edge_ellipse[1][1]
            cnt+=1  
            #钟表外圈拟合椭圆的旋转角度
            clock_feature[cnt]=edge_ellipse[2]
            cnt+=1  
            #钟表外圈起点和终点的距离
             #clock_feature[cnt]=count_distance(clean_edge_strokes[0,0],clean_edge_strokes[0,1],clean_edge_strokes[-1,0],clean_edge_strokes[-1,1])
             #取外圈笔画前三分之一段和后三分之一段求最短距离
            clock_feature[cnt]=get_cloest_distance(clean_edge_strokes[:int(clean_edge_strokes.shape[0]/3),:2],clean_edge_strokes[int(clean_edge_strokes.shape[0]*2/3):,:2])
            cnt+=1  
            #钟表外圈起点和终点的角度差
            clock_feature[cnt]=math.fabs(get_polar_coordinates(clean_edge_strokes[0],center)[1]-get_polar_coordinates(clean_edge_strokes[-1],center)[1])
            cnt+=1
        else:
            cnt+=8
        #指针特征
        temp_hand_indexs=list(itertools.chain(*hand_area_indexs))
        if len(temp_hand_indexs)>0:  
            #调用函数获取指针三个点
            hand_strokes=merge_multiple_strokes(strokes,internal_indexs,temp_hand_indexs)
            hour_hand,minute_hand,hand_center = self.hand_detector.hand_detect(hand_strokes)
            hour_hand_angle=get_polar_coordinates(hour_hand,hand_center)[1]
            minute_hand_angle=get_polar_coordinates(minute_hand,hand_center)[1]
            #hour_hand,minute_hand,hand_center=[1,0],[0,1],[10,10]
            min_hand_indexs=min(temp_hand_indexs)
            if min_hand_indexs>0:
                #画时针之前到画第一笔时针的间隔时间
                clock_feature[cnt]=math.fabs(strokes[strokes_indexs[min_hand_indexs,1]-1,2]-strokes[strokes_indexs[min_hand_indexs-1,1]-1,2])
            cnt+=1
            #区分时针分针
            if(hour>=10):
                hour-=10
            
            if len(digit_info[hour])>0:         
                hour_digit_angles=np.zeros(len(digit_info[hour]))
                for i in range(len(digit_info[hour])):
                    digit_strokes=merge_multiple_strokes(strokes,internal_indexs,digit_area_indexs[digit_info[hour][j][0]])
                    digit_center=count_center(digit_strokes)
                    hour_digit_angles[i]=get_polar_coordinates(digit_center,hand_center)[1]
            else:
                hour_digit_angles=[0]
            minute=int((minute/5)%10)
            if len(digit_info[minute])>0:
                minute_digit_angles=np.zeros(len(digit_info[minute]))
                for i in range(len(digit_info[minute])):
                    digit_strokes=merge_multiple_strokes(strokes,internal_indexs,digit_area_indexs[digit_info[minute][j][0]])
                    digit_center=count_center(digit_strokes)
                    minute_digit_angles[i]=get_polar_coordinates(digit_center,hand_center)[1]
            else:
                minute_digit_angles=[0]
            #计算各自与正确角度的夹角
            first_hour_bias=min([math.fabs(hour_hand_angle-hour_digit_angle) for hour_digit_angle in hour_digit_angles])
            first_minute_bias=min([math.fabs(minute_hand_angle-minute_digit_angle) for minute_digit_angle in minute_digit_angles])
            second_hour_bias=min([math.fabs(minute_hand_angle-hour_digit_angle) for hour_digit_angle in hour_digit_angles])
            second_minute_bias=min([math.fabs(hour_hand_angle-minute_digit_angle) for minute_digit_angle in minute_digit_angles])
            if first_hour_bias+first_minute_bias<=second_hour_bias+second_minute_bias:     
                #时针与正确角度的差值
                clock_feature[cnt]=first_hour_bias
                cnt+=1
                #分针与正确角度的差值
                clock_feature[cnt]=first_minute_bias
                cnt+=1
            else:
                #时针与正确角度的差值
                clock_feature[cnt]=second_hour_bias
                cnt+=1
                #分针与正确角度的差值
                clock_feature[cnt]=second_minute_bias
                cnt+=1
                #交互两个指针
                hour_hand,minute_hand=minute_hand,hour_hand
            #时针长度与分针长度的比值
            clock_feature[cnt]=count_distance(hour_hand[0],hour_hand[1],hand_center[0],hand_center[1])/count_distance(minute_hand[0],minute_hand[1],hand_center[0],hand_center[1])
            cnt+=1
        else:
            cnt+=4
        #总笔画数
        clock_feature[cnt]=strokes_indexs.shape[0]
        #print("total strokes cnt",cnt)
        cnt+=1
        #总笔画长度
        clock_feature[cnt]=count_stroke_length(strokes)
        #print("total length cnt",cnt)
        cnt+=1
        #总笔画时间
        for i in range(strokes_indexs.shape[0]):
            clock_feature[cnt]+=strokes[strokes_indexs[i,1]-1,2]-strokes[strokes_indexs[i,0],2] 
        #print("total strokes time cnt",cnt)
        cnt+=1
        #总绘画速度
        clock_feature[cnt]=clock_feature[cnt-2]/clock_feature[cnt-1]
        cnt+=1
        #总实验时间
        clock_feature[cnt]=strokes[strokes_indexs[-1,1]-1,2]-strokes[strokes_indexs[0,1],2]
        #print("total test time cnt",cnt)
        cnt+=1
        #总思考时间
        clock_feature[cnt]=clock_feature[cnt-1]-clock_feature[cnt-3]
        cnt+=1
        #总思考时间与总实验时间比值
        clock_feature[cnt]=clock_feature[cnt-1]/clock_feature[cnt-2]
        cnt+=1
        #print("cnt",cnt)

        self.draw_result_picture(strokes,strokes_indexs,internal_indexs,digit_area_indexs,edge_ellipse,buffer)
        return clock_feature[:cnt],tol_digit_num

    # 展示测试结果图片
    def draw_result_picture(self,strokes,strokes_indexs,internal_indexs,digit_area_indexs,edge_ellipse,buffer):
        plt.cla()
        ax = plt.gca()
        ax.cla()
        for index in strokes_indexs:
            plt.plot(strokes[index[0]:index[1],0],strokes[index[0]:index[1],1], color="black")
            
        brounding_box=np.zeros((5,2))
        for area in digit_area_indexs:
            area_storke=merge_multiple_strokes(strokes,internal_indexs,area)
            clean_area_storke=area_storke[np.where(area_storke[:,0]>=0)]
            minx,maxx,miny,maxy,mint,maxt=get_bounding_box(clean_area_storke)
            brounding_box[0]=(minx,miny)
            brounding_box[1]=(minx,maxy)
            brounding_box[2]=(maxx,maxy)
            brounding_box[3]=(maxx,miny)
            brounding_box[4]=(minx,miny)
            plt.plot(brounding_box[:,0],brounding_box[:,1], color="skyblue")

        ellipse=Ellipse(edge_ellipse[0],edge_ellipse[1][0],edge_ellipse[1][1],edge_ellipse[2])
        ellipse.set_color("teal")
        ellipse.set_fill(False)
        ax.add_artist(ellipse)
        # plt.savefig(save_path)
        plt.show()
        fig = plt.gcf()
        fig.set_size_inches(4, 4)  # 设置图片的尺寸为400 * 400
        fig.savefig(buffer, format="jpg")
        plt.close('all')

    

    #若数字数目不够，认为当前的数字都应该采用
    #如果数字数目过多，根据数字分布筛出
    def choose_clock_digit(self,digit_info,digit_angles,digit_size,digit_area_indexs,digit_label):
        clock_digit_area_info=np.empty((13,2))*np.nan
        error_digit_info=[]
        digit_size_difference=self.get_digit_status(digit_info,digit_size)[0]
        #所有区域按照对应的数字及其极坐标角度theta排序
        for i in range(len(digit_info)):
            digit_info[i]=sorted(digit_info[i],key=(lambda x:x[3]))
        #min_perfect_digit=-1
        #数字3-9都有且仅有一个,先找出3-9
        for i in range(3,10):
            #数字i正好一个直接取用
            if digit_size_difference[i]==0:
                clock_digit_area_info[i]=digit_info[i][0][0],digit_info[i][0][3]
        for i in range(3,10):
            #数字i多于一个取
            if digit_size_difference[i]<0:
                #选出角度最符合的区域
                smaller_digit_theta=clock_digit_area_info[:i,1]
                smaller_digit_theta[smaller_digit_theta<90]+=360
                smaller_digit_theta=np.sort(smaller_digit_theta[~np.isnan(smaller_digit_theta)])
                bigger_digit_theta=clock_digit_area_info[i+1:,1]
                bigger_digit_theta=np.sort(bigger_digit_theta[~np.isnan(bigger_digit_theta)])
                digit_score=np.zeros(len(digit_info[i]))
                for j in range(len(digit_info[i])):
                    digit_score+=np.where(smaller_digit_theta<digit_info[i][j][3])[0].size
                    digit_score+=np.where(bigger_digit_theta>digit_info[i][j][3])[0].size
                min_digit_score_indexs=int(np.argmin(digit_score))
                clock_digit_area_info[i]=digit_info[i][min_digit_score_indexs][0],digit_info[i][min_digit_score_indexs][3]
                for j in range(len(digit_info[i])):
                    if j!=min_digit_score_indexs:
                        error_digit_info.extend(digit_info[i][j])
                        digit_info[i][j]=[]
        #处理数字0-2
        for i in range(3):
            #数字的数目正好或是缺失则采用全部现有数字
            if digit_size_difference[i]>=0:
                continue
            #数字多则取到偏离数字应该在的空间分布角度最小的
            temp_digit_difference_angles=np.zeros((len(digit_info[i])))
            for j in range(len(digit_info[i])):
                temp_digit_difference_angles[j]=min([math.fabs(digit_info[i][j][3]-x) for x in digit_angles[i]])
            while(digit_size_difference[i]<0):
                max_theta_index=np.argmax(temp_digit_difference_angles)
                temp_digit_difference_angles[max_theta_index]=-1
                error_digit_info.extend(digit_info[i][max_theta_index])
                digit_info[i][max_theta_index]=[]
                digit_size_difference[i]+=1
        for i in range(len(digit_info)):
            digit_info[i]=[x for x in digit_info[i] if x]
        return digit_info,error_digit_info

    #根据label将笔画集合成区域
    def get_areas_indexs(self,strokes,indexs,label):
        area_indexs=[]
        tmp=[]
        for i in range(indexs.shape[0]-1):
            if label[i]==1:
                tmp.append(i)
                area_indexs.append(tmp)
                tmp=[]
            else:
                tmp.append(i)
        tmp.append(indexs.shape[0]-1)
        area_indexs.append(tmp)
        length=len(area_indexs)
        tmp=area_indexs.copy()
        changelist=[]
        #论文中的Detecting Overwriting and Augmentation
        for i in range(length):
            if i in changelist:
                continue
            a=strokes[indexs[area_indexs[i][0],0]:indexs[area_indexs[i][-1],1],:2]
            for j in range(i+1,length):
                b=strokes[indexs[area_indexs[j][0],0]:indexs[area_indexs[j][-1],1],:2]
                overlap_score=overlap(a,b)
                #无重叠面积
                if dcmp(overlap_score)==0:
                    continue
                if overlap_score>0.6:
                    tmp.pop(i)
                    break
                else:
                    if overlap_score>0.05:
                        tmp[i].extend(tmp[j])
                        tmp.pop(j)
                        changelist.append(j)
                        continue    
        return tmp

    #修复过度划分的区域
    def repair_over_split(self,strokes,internal_indexs,digit_area_indexs,digit_label,center):
        digit_info=self.digit_label_to_list(strokes,internal_indexs,digit_area_indexs,digit_label,center)
        error_area,adequate_digit,lack_digit=self.get_error_area_and_lack_digit(digit_info,self.digit_size,0)
        if not error_area:
            return  digit_area_indexs,digit_label
        #判断是否过度划分区域
        for i in range(len(error_area)):
            for j in range(i+1,len(error_area)):
                if not error_area[i] or not error_area[j]:
                    continue
                if math.fabs(error_area[i][2]-error_area[j][2])<=30 and math.fabs(error_area[i][3]-error_area[j][3])<=15 :
                    merge_strokes=merge_multiple_strokes(strokes,internal_indexs,
                                digit_area_indexs[error_area[i][0]]+digit_area_indexs[error_area[j][0]])
                    #draw_by_strokes(strokes,digit_indexs,area_indexs[error_area[i][0]]+area_indexs[error_area[j][0]])
                    #merge_feature=make_digit_feature(merge_strokes).reshape(1,24)
                    #merge_score=digit_predict(merge_feature,graph,sess)
                    merge_feature=self.digit_detector.make_feature(merge_strokes).reshape(1,24)
                    merge_score=self.digit_detector.predict_by_feature(merge_feature)
                    if  self.check_merge_status(error_area[i],error_area[j],merge_score,adequate_digit,lack_digit,0):
                        temp_list=[error_area[i][0],merge_score[0,1],(error_area[i][2]+error_area[j][2])/2,(error_area[i][3]+error_area[j][3])/2]
                        digit_info[error_area[i][4]][error_area[i][5]]=[]
                        digit_info[error_area[j][4]][error_area[j][5]]=[]
                        digit_info[int(merge_score[0,0])].append(temp_list)
                        digit_area_indexs[error_area[i][0]].extend(digit_area_indexs[error_area[j][0]])
                        digit_area_indexs[error_area[j][0]]=[]
                        digit_label[error_area[j][0]]=-1
                        digit_label[error_area[i][0]]=merge_score[0,:]
                        error_area[i]=error_area[j]=[]
                        break
        digit_label=digit_label[np.where(digit_label[:,0]>=0)]
        digit_area_indexs=[x for x in digit_area_indexs if x]
        return  digit_area_indexs,digit_label

    #判断是否应该合并区域
    #area_info(area_index,置信度，极坐标r,theta,对应数字，digit_info_index)
    def check_merge_status(self,area_info1,area_info2,merge_score,adequate_digit,lack_digit,times):
        #特殊情况
        if area_info1[4]==1 and area_info2[4]==1 and (merge_score[0,0]==0 or merge_score[0,0]==1 or merge_score[0,0]==8):
            return False
        if area_info1[4]==0 and area_info2[4]==0 and (merge_score[0,0]==0 or merge_score[0,0]==1):
            return False
        if ((area_info1[4]==1 and area_info2[4]==0) or (area_info1[4]==0 and area_info2[4]==1))and (merge_score[0,0]==0 or merge_score[0,0]==1 or merge_score[0,1]<=0.8):
            return False
        #效果增强
        if int(merge_score[0,0])==area_info1[4] and merge_score[0,1]>0.9:
            return True
        if int(merge_score[0,0])==area_info2[4] and merge_score[0,1]>0.9:
            return True
        if times==1:
            return False
        #if area_info1[4]==1 and area_info2[4]==1 and merge_score[0,0] not in lack_digit:
        #    return False;
        '''
        #如果合并分数大于均值且被合并区域不是唯一的
        if merge_score[0,1]>=(area_info1[1]+area_info2[1])/2 and area_info1[4] not in adequate_digit and area_info2[4] not in adequate_digit :
            return True
            '''
        #如果合并的结果正好是缺失的数字则合并
        if int(merge_score[0,0]) in lack_digit and merge_score[0,1]>0.5:
            return True
        return False

    #修复欠划分的区域
    def repair_under_split(self,strokes,internal_indexs,digit_area_indexs,digit_label,center):
        digit_info=self.digit_label_to_list(strokes,internal_indexs,digit_area_indexs,digit_label,center)
        under_split_areas=[]
        for i in range(len(digit_info)):
            '''
            if (i==4 or i==5) and len(digit_info[i])==1:
                continue'''
            under_split_areas.extend([x+[i,j] for j,x in enumerate(digit_info[i]) if x])
        under_split_areas=sorted(under_split_areas,key=(lambda x: (len(digit_area_indexs[x[0]]),x[3])))
        digit_size_difference,adequate_digit,lack_digit=self.get_digit_status(digit_info,self.digit_size)
        for under_split_area in under_split_areas:
            if len(digit_area_indexs[under_split_area[0]])<=1:
                continue
            child_areas=get_real_child(digit_area_indexs[under_split_area[0]])
            child_score=np.zeros(len(child_areas))
            child_result=np.zeros((len(child_areas),len(digit_area_indexs[under_split_area[0]]),2))
            #i 代表第 i 个方案
            for i in range(len(child_areas)):
                child_digit_size_difference=list(digit_size_difference)
                for j in range(len(child_areas[i])):
                    split_strokes=merge_multiple_strokes(strokes,internal_indexs,child_areas[i][j])
                    #draw_by_strokes(strokes,internal_indexs,child_areas[i][j])
                    #split_feature=make_digit_feature(split_strokes).reshape(1,24)
                    #child_result[i][j]=digit_predict(split_feature,graph,sess)[0,:]
                    split_feature=self.digit_detector.make_feature(split_strokes).reshape(1,24)
                    child_result[i][j]=self.digit_detector.predict_by_feature(split_feature)[0,:]
                    #分出的数字在缺失的列表
                    if child_digit_size_difference[int(child_result[i][j][0])]>0:
                        child_score[i]+=100
                    elif child_digit_size_difference[int(child_result[i][j][0])]==0:
                        child_score[i]+=10
                    else:
                        child_score[i]+=1
                    child_digit_size_difference[int(child_result[i][j][0])]-=1
            max_split_score_index=np.argmax(child_score).astype(int)
            #max_split_score=child_score[max_split_score_index]
            if self.check_over_split_status(under_split_area,digit_size_difference,adequate_digit,lack_digit,child_areas[max_split_score_index],child_result[max_split_score_index],child_score[max_split_score_index]):
                digit_area_indexs[under_split_area[0]]=[]
                digit_label[int(under_split_area[0])]=-1
                child_label=np.zeros((len(child_areas[max_split_score_index]),2))
                digit_area_indexs.extend(child_areas[max_split_score_index])
                for j in range(len(child_areas[max_split_score_index])):
                    child_label[j]=child_result[max_split_score_index][j]
                digit_label=np.concatenate((digit_label,child_label))
                digit_info=self.digit_label_to_list(strokes,internal_indexs,digit_area_indexs,digit_label,center)
                digit_size_difference,adequate_digit,lack_digit=self.get_digit_status(digit_info,self.digit_size)
                under_split_area=[]
        digit_label=digit_label[np.where(digit_label[:,0]>=0)]
        digit_area_indexs=[x for x in digit_area_indexs if x]
        return digit_area_indexs,digit_label

    #判断区域是否应该划分
    def check_over_split_status(self,under_split_area,digit_size_difference,adequate_digit,lack_digit,child_area ,child_result,child_score):
        #分出的数字全是缺少的数字
        if child_score>= len(child_area)*100:
            return True
        #原来区域对应的数字的状态 0 over 1 adeguate 2 lack
        orgin_flag=0
        if under_split_area[4] in adequate_digit:
            orgin_flag=1
        elif under_split_area[4] in lack_digit:
            orgin_flag=2
        if orgin_flag == 0:
            if child_score>=100:
                return True
        if orgin_flag ==1:
            if under_split_area[4] in child_result and child_score>=100:
                return True
        if orgin_flag ==2:
            if child_score>=200:
                return True
        return False

    #获取当前钟表数字的数目状态
    def get_digit_status(self,digit_info,digit_size):
        digit_size_difference=[digit_size[i]-len(x) for i,x in enumerate(digit_info)]
        lack_digit=[i for i,x in enumerate(digit_size_difference) if x>0]
        adequate_digit=[i for i,x in enumerate(digit_size_difference) if x==0]
        return digit_size_difference,adequate_digit,lack_digit


    def digit_label_to_list(self,strokes,digit_indexs,area_indexs,digit_label,center):
        #存储数字的信息，第x行对应数字x，每一列中为四维tuple(对应的区域index,置信度,以中心为原点的极坐标 r,theta)
        digit_info=[]
        for i in range(10):
            digit_info.append([])
        for i in range(len(area_indexs)):
            digit_strokes=merge_multiple_strokes(strokes,digit_indexs,area_indexs[i])
            digit_center=count_center(digit_strokes)
            r,theta=get_polar_coordinates(digit_center,center)
            digit_info[int(digit_label[i,0])].append([i,digit_label[i,1],r,theta])
        #每一行按置信度，r从大到小排序
        for i in range(len(digit_info)):
            digit_info[i]=sorted(digit_info[i],key=(lambda x:(x[1],x[2])),reverse=True)
        return digit_info

    #获取可能划分错误的区域，1.区域对应数字的个数过多 2.区域得分低
    # 和缺失的数字
    def get_error_area_and_lack_digit(self,digit_info,digit_size,times):
        error_area=[]
        lack_digit=[]
        adequate_digit=[]
        '''
        if times ==1:
            for i in range(len(digit_info)):
                if len(digit_info[i])>digit_size[i]:
                    #区域对应数字的个数过多
                    error_area.extend([ x+[i,j] for j,x in enumerate(digit_info[i]) if x])
                elif len(digit_info[i])<digit_size[i]:
                    #贪心，数字缺失时对应的区域认为没有错误
                    lack_digit.append(i)
                else:
                    adequate_digit.append(i)
                    #区域得分低
                    error_area.extend([x+[i,j] for j,x in enumerate(digit_info[i]) if x and x[1]<=0.9])
        else:
        '''
        for i in range(len(digit_info)):
            error_area.extend([x+[i,j] for j,x in enumerate(digit_info[i]) if x])
            if len(digit_info[i])<digit_size[i]:
                lack_digit.append(i)
            else:
                adequate_digit.append(i)         
        #可能错误区域按极坐标系theta ,r 从大到小排序
        error_area=sorted(error_area,key=(lambda x:(x[3],x[2])))
        return error_area,adequate_digit,lack_digit

    #获取可能的欠划分区域
    def get_under_split_area(self,digit_info,digit_size):
        lack_digit=[i for i,x in enumerate(digit_info) if len(x)<digit_size[i]]
        adequate_digit=[i for i,x in enumerate(digit_info) if len(x)==digit_size[i]]
        under_split_area=[]
        for i in range(len(digit_info)):
            #if len(digit_info[i])>digit_size[i]:
            #print(digit_info[i])
            under_split_area.extend([x+[i,j] for j,x in enumerate(digit_info[i]) if x])
        under_split_area=sorted(under_split_area,key=(lambda x:(x[3],x[2])))
        return under_split_area,adequate_digit,lack_digit

    
    '''
    #论文方法未采用，如果要使用需要进一步修改
    #修复划分不全面的区域
    def repair_under_segmentation(strokes,strokes_indexs,area_indexs,st_slice,score):
        child=get_real_child(area_indexs(st_slice))
        child_length=len(  child)
        child_score=np.zeros((child_length))
        for i in range(child_length):
            cur_score=0
            for j in range(len(child[i])):
                tmp_feature=make_digit_feature(merge_multiple_strokes(strokes,strokes_indexs,child[i][j]))
                cur_score+=predict(tmp_feature)[1]
            child_score[i]=cur_score/len(child[i])
        #有可能多个最大值
        max_indexs=np.where(child_score==np.max(child_score))
        if child_score[max_indexs[0]]<score:
            return area_indexs,score
        tmp=child[max_indexs[0]]
        for j in range(len(child[max_indexs[0]])):
            first_merge_strokes=merge_multiple_strokes(strokes,strokes_indexs,child[max_indexs[0]][j])
            for k in range(j,len(child[max_indexs[0]])):
                second_merge_strokes=merge_multiple_strokes(strokes,strokes_indexs,child[max_indexs[0]][k])
                overlap_score=overlap(first_merge_strokes,second_merge_strokes)
                if overlap_score>0.6:
                    tmp.pop(j)
                    break
        area_indexs.pop(st_slice)
        for i in range(len(tmp)):
            area_indexs.insert(i+st_slice,tmp[i])
        return area_indexs,overlap_score
    #论文方法未使用，如果要使用需要进一步修改
    #修复过度划分的区域
    def repair_over_segmentation(strokes,strokes_indexs,area_indexs,first,second):
        merge_list=area_indexs[first]+area_indexs[second]
        merge_strokes=merge_multiple_strokes(strokes,strokes_indexs,merge_list)
        merge_feature=make_digit_feature(merge_strokes)
        merge_score=predict(merge_feature)
        return area_indexs,merge_score
    #画图
    def draw_result_picture_with_digit(self,strokes,strokes_indexs,kmeans_label,svm_label,digit_label,digit_area_indexs,hand_area_indexs,save_path):
        #cnt=0
        #钟表外沿坐标
        plate_indexs=strokes_indexs[kmeans_label==1]
        #cnt=plate_indexs.shape[0]
        plt.cla()
        for i in range(plate_indexs.shape[0]):
            plt.plot(strokes[plate_indexs[i, 0]:plate_indexs[i, 1], 0],
                    strokes[plate_indexs[i, 0]:plate_indexs[i, 1], 1], color="black")
        digit_indexs=strokes_indexs[kmeans_label!=1]
        for i in range(len(hand_area_indexs)):
            for j in range(len(hand_area_indexs[i])):
                plt.plot(strokes[digit_indexs[hand_area_indexs[i][j], 0]:digit_indexs[hand_area_indexs[i][j], 1], 0],
                    strokes[digit_indexs[hand_area_indexs[i][j], 0]:digit_indexs[hand_area_indexs[i][j], 1], 1], 
                        color="red")

        brounding_box=np.zeros((5,2))
        for i in range(len(digit_area_indexs)):
            minx,miny=INF,INF
            maxx,maxy=0,0
            #画出区域内的笔画
            for j in range(len(digit_area_indexs[i])):
                curbox=get_bounding_box(strokes[digit_indexs[digit_area_indexs[i][j], 0]:digit_indexs[digit_area_indexs[i][j], 1],:])
                minx=min(curbox[0],minx)
                maxx=max(curbox[1],maxx)
                miny=min(curbox[2],miny)
                maxy=max(curbox[3],maxy)
                plt.plot(strokes[digit_indexs[digit_area_indexs[i][j], 0]:digit_indexs[digit_area_indexs[i][j], 1], 0],
                    strokes[digit_indexs[digit_area_indexs[i][j], 0]:digit_indexs[digit_area_indexs[i][j], 1], 1], 
                        color="darkgreen")
            brounding_box[0]=(minx,miny)
            brounding_box[1]=(minx,maxy)
            brounding_box[2]=(maxx,maxy)
            brounding_box[3]=(maxx,miny)
            brounding_box[4]=(minx,miny)
            plt.plot(brounding_box[:,0],brounding_box[:,1], color="skyblue")
            if i%2==0:
                plt.text(minx,maxy+10,'%1.0f'%digit_label[i,0]+" "+'%.2f'%digit_label[i,1])
            else:
                plt.text((minx+maxx)/2,(maxy+miny)/2,'%1.0f'%digit_label[i,0]+" "+'%.2f'%digit_label[i,1])
        #plt.savefig(save_path)
        plt.show()
    '''
    





    
if __name__ == "__main__":
    path =r'D:\Code\python\草图论文复现\data'
    cdt_model=CdtModel()
    for d in range(1,5):
        for root, dirs, files in os.walk(path+"\\"+str(d), topdown=False):
            for name in files:
                if name.endswith(".csv"):
                    indexs_=name.rfind('_',0,len(name))
                    if name[indexs_+1]=='1':
                        new_name=name[:indexs_+1]+'2'+name[indexs_+2:]
                        if new_name in  files:
                            command_strokes=np.loadtxt(open(os.path.join(root, name),"rb"),delimiter=",",skiprows=0)
                            copy_strokes=np.loadtxt(open(os.path.join(root, new_name),"rb"),delimiter=",",skiprows=0)
                            cdt_model.make_cdt_feature(command_strokes,copy_strokes,10,11)