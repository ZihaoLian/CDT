import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial

#工具包

INF=0x7fffffff
eps=1e-8

#以center为极点，x轴正方向为极轴，给出digit_center的极坐标
def get_polar_coordinates(digit_center,center):
    r=count_distance(digit_center[0],digit_center[1],center[0],center[1])
    theta=math.degrees(math.atan((digit_center[1]-center[1])/(digit_center[0]-center[0])))
    if digit_center[0]<center[0]:
        theta+=180
    elif digit_center[1]<center[1]:
        theta+=360
    return r,theta

#求欧式距离
def count_distance(x,y,tx,ty):
    return math.sqrt((x-tx)**2+(y-ty)**2)

#找出笔画包围盒 bounding box
def get_bounding_box(stroke):
    #cleaned_storke=strokes[np.where(stroke[:,0]>=0)]
    minx,miny,mint=stroke.min(axis=0)
    maxx,maxy,maxt=stroke.max(axis=0)
    return minx,maxx,miny,maxy,mint,maxt

#合并多个区域的笔画
def merge_multiple_strokes(strokes,strokes_indexs,merge_list):
    merge=np.zeros((strokes.shape[0],3))
    start=0
    end=0
    for i in range(len(merge_list)):
        end+=strokes_indexs[merge_list[i],1]-strokes_indexs[merge_list[i],0]+1
        merge[start:end,:]=strokes[strokes_indexs[merge_list[i],0]:strokes_indexs[merge_list[i],1]+1,:]
        start=end
    return merge[:end,:]

#求区域线段总长度
def count_stroke_length(strokes):
    tol_length=0
    cur=strokes[0]
    for i in range(1,strokes.shape[0]):
        if (cur[0]>=0) and (strokes[i,0]>=0):
            tol_length+=count_distance(cur[0],cur[1],strokes[i,0],strokes[i,1])
        cur=strokes[i]
    return tol_length
#计算两个序列之间的最短距离,O(nlogn)
def get_cloest_distance(array1,array2):
    len1=array1.shape[0]
    #len2=array2.shape[0]
    array=np.insert(np.r_[array1,array2],2, values=0, axis=1)
    array[len1:,2]=1
    array=array[np.lexsort([array[:,1],array[:,0]]),:]
    return count_cloest_distance(array)
def count_cloest_distance(array):
    len=array.shape[0]
#    print(len)
    if len<=1 :
        return INF
    if len==2 :
        if  array[0,2]==array[1,2]:
            return INF
        else :
              return count_distance(array[0][0],array[0][1],array[1][0],array[1][1])
    mid=int(len/2)
    midx=array[mid,0] 
    left=count_cloest_distance(array[0:mid,:])
    right=count_cloest_distance(array[mid:,:])
    left=min(left,right)
    strip=array[np.where(abs(array[:,0]-midx)<left)]
    strip=strip[np.lexsort([strip[:,1]]),:]
    for i in range(strip.shape[0]):
        for j in range(i+1,strip.shape[0]):
            if strip[j,1]-strip[i,1]>=left:
                continue
            if strip[j,2]==strip[i,2]:
                continue
            left=min(left,count_distance(strip[i][0],strip[i][1],strip[j][0],strip[j][1]))
    return left  

#画出一笔
def draw_by_strokes(strokes,digit_indexs,area_list):
    plt.cla()
    for i in area_list:
            plt.plot(strokes[digit_indexs[i, 0]:digit_indexs[i, 1], 0],
                 strokes[digit_indexs[i, 0]:digit_indexs[i, 1], 1], 
                     color="black")
    plt.show()

#求点序列代表的面积点，序列a内的点要按顺时针或逆时针给出
def polygon_area(a):
    x=a[:,0]
    y=a[:,1]
    correction = x[-1] * y[0] - y[-1]* x[0]
    main_area = np.dot(x[:-1], y[1:]) - np.dot(y[:-1], x[1:])
    return 0.5*np.abs(main_area + correction)

#浮点数判断符号
def dcmp(x):
    if x>eps:
        return 1
    else:
        if x<-eps:
            return -1
        else:
            return 0

#叉乘 ac X bc
def cross(a,b,c):
    return (a[0]-c[0])*(b[1]-c[1])-(b[0]-c[0])*(a[1]-c[1])

#两线段交点,a,b,c,d分别为两线段的端点
def intersection(a,b,c,d):
    p=a.copy()
    t =((a[0]-c[0])*(c[1]-d[1])-(a[1]-c[1])*(c[0]-d[0]))/((a[0]-b[0])*(c[1]-d[1])-(a[1]-b[1])*(c[0]-d[0]))
    p[0] +=(b[0]-a[0])*t
    p[1] +=(b[1]-a[1])*t
    return p

#在点序列a末尾增加点b
def add_one_point(a,b):
    tmp=np.zeros((a.shape[0]+1,a.shape[1]))
    tmp[:a.shape[0],:]=a
    tmp[a.shape[0],:]=b
    return tmp

#两三角形重叠面积
def CPIA(a,b):
    na=a.shape[0]
    nb=b.shape[0]
    a=add_one_point(a,a[0])
    b=add_one_point(b,b[0])
    p=b.copy()
    tmp=np.zeros((20,2))
    for i in range(na):
        if nb<=2:
            break
        sflag=dcmp(cross(a[i+1],p[0],a[i]))
        for j in range(nb):
            tn=0
            if sflag>=0:
                tmp[tn]=p[j]
                tn+=1
            eflag=dcmp(cross(a[i+1],p[j+1],a[i]))
            if (sflag^eflag)==-2:
                tmp[tn]=intersection(a[i],a[i+1],p[j],p[j+1])
            sflag=eflag 
        nb=tn
        p=tmp.copy()
        p=add_one_point(p,p[0])   
    if nb<3:
        return 0.0
    return polygon_area(p)

#任意多边形顶点序列a,b,点序列内点要按顺时针或逆时针给出
#遍历多边形a,b内的三角形，求三角形交
def SPIA(a,b):
    na=a.shape[0]
    nb=b.shape[0]
    a=add_one_point(a,a[0])
    b=add_one_point(b,b[0])
    t1=np.zeros((4,2))
    t2=np.zeros((4,2))
    res=0.0
    t1[0]=a[0]
    t2[0]=b[0]
    for i in range(2,na):
        t1[1]=a[i-1]
        t1[2]=a[i]
        num1=dcmp(cross(t1[1],t1[2],t1[0]))
        if num1<0:
            t1[1],t1[2]=t1[2],t1[1]
        for j in range(2,nb):
            t2[1]=b[j-1]
            t2[2]=b[j]
            num2=dcmp(cross(t2[1],t2[2],t2[0]))
            if num2<0:
                t2[1],t2[2]=t2[2],t2[1]
            res+=CPIA(t1[:3],t2[:3])*num1*num2
    return res

#两个点序列的凸包面积交除凸包面积并
def overlap(a,b):
    a=a[np.where(a[:,0]>=0)]
    b=b[np.where(b[:,0]>=0)]
    #点个数少于3
    if(a.shape[0]<3 or b.shape[0]<3):
        return 0.0
    #点序列无凸包，即点序列的x坐标或y坐标完全相等
    if(np.all(a[:,0] == a[0,0],axis=0)or np.all(a[:,1] == a[0,1],axis=0)):
        return 0.0
    if(np.all(b[:,0] == b[0,0],axis=0)or np.all(b[:,1] == b[0,1],axis=0)):
        return 0.0
    #print("a",a)
    #print("b",b)
    a=a[spatial.qhull.ConvexHull(a,qhull_options="QJ").vertices]
    b=b[spatial.qhull.ConvexHull(b,qhull_options="QJ").vertices]
    area=polygon_area(a)
    overlap_area=SPIA(a,b)
    if dcmp(area)==0:
        return 0.0
    return overlap_area/area

#寻找所有笔画中心
def count_center(strokes):
    arr=strokes[np.where(strokes[:,0]>=0)]
    ans=np.sum(arr,axis=0)
    return ans[0]/arr.shape[0],ans[1]/arr.shape[0]


#连续真子集
#复杂度极高 O(n2^n),但一般n不超过5，n极限值应该在30以下待改
def get_real_child(father_list):
    length=len(father_list)
    child_list = []
    for i in range(1,1<<(length-1)):
        tmp_list=[]
        #tmp=i
        end=length
        start=length-1
        while(i):
            if i&1:
                tmp_list.insert(0,father_list[start:end])
                end=start
            start-=1
            i>>=1
        tmp_list.insert(0,father_list[0:end])
        child_list.append(tmp_list)      
    return child_list

#获取笔画起始位置和终止位置，前闭后开
def get_strokes_index(strokes):
    len=strokes.shape[0]
    indexs=np.zeros((len,2),dtype=np.int32)  #笔画起始位置和终止位置
    cnt=0 #笔画总数
    start=0
    for i in range(len):
        #要根据标记位更改
        if strokes[i][0]<0:
            indexs[cnt][0]=start
            indexs[cnt][1]=i
            start=i+1
            cnt+=1
    return indexs[:cnt,:]