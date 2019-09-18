import math
import numpy as np
from cdt_util import count_distance
from cdt_util import count_stroke_length
import tensorflow as tf
import cv2
from sklearn.utils.extmath import softmax

class DigitDetector:

    def __init__(self):
        self.graph,self.sess=self.loadModel('./ckpt_cdt/cdt.ckpt-31300.meta','./ckpt_cdt/')

    #等弧长8点
    def make_feature(self,strokes):
        #print("strokes",strokes)
        tol_length=count_stroke_length(strokes)
        average=tol_length/8
        sample=np.zeros(24)
        cnt=0
        sample[cnt:cnt+3]=strokes[0].reshape(3)
        flag=False
        #print(average)
        cnt+=3
        cur=strokes[0]
        cur_length=0    
        for i in range(1,strokes.shape[0]):
            if cnt>=24:
                return sample
            if (cur[0]>0) and (strokes[i,0]>0):
                if flag:
                    flag=False
                    sample[cnt:cnt+3]=cur.reshape(3)
                    cnt+=3
                    continue
                cur_length+=count_distance(cur[0],cur[1],strokes[i,0],strokes[i,1])
                if cur_length > average :
                    sample[cnt:cnt+3]=strokes[i].reshape(3)
                    cnt+=3
                    cur_length=0
            else:
                flag=True           
            cur=strokes[i] 
        temp=-1
        while cur[0]<0:
            temp-=1
            cur=strokes[temp].reshape(3)
        while cnt<24:
            sample[cnt:cnt+3]=cur
            cnt+=3
        return sample

    #根据单一笔画识别
    def predict_by_data(self,storke):
        eightPoint=self.make_feature(storke)
        return self.digit_predict(eightPoint,self.graph,self.sess)
        
    #根据特征识别
    def predict_by_feature(self,features):
        return self.digit_predict(features,self.graph,self.sess)
    
    def digit_predict(self,eightPoint,graph,sess):
        X_img = self.drawImage(eightPoint)
        X_img=np.array(X_img).reshape(-1,28,28,1)
        #graph,sess = loadModel(metaPath,ckptPath)
        Variable_2 = graph.get_tensor_by_name('Variable_2:0')
        # print(sess.run(Variable_2))
        scores = graph.get_tensor_by_name('Squeeze:0')
        pred = sess.run(scores,feed_dict={'Placeholder:0': X_img,'Placeholder_2:0':False})
        if pred.ndim==1:
            pred=pred.reshape((1,pred.shape[0]))
        pred=softmax(pred)
        label=np.zeros((pred.shape[0],2))
        label[:,0]=np.argmax(pred, axis=1).astype(int)
        label[:,1]=np.max(pred, axis=1)
        return label
    
    def drawImage(self,eightPoint):
        X_img = []
        for k in range(len(eightPoint)):
            each_x=[eightPoint[k][3*i] for i in range(8)]
            each_x = (each_x - np.mean(each_x)) 
            each_x_std = np.max(np.abs(each_x))
            if each_x_std == 0:
                each_x = each_x + 50
            else:   
                each_x = each_x / each_x_std * 50 + 50
            
            each_y = [eightPoint[k][3 * i + 1] for i in range(8)]
            each_y = (each_y - np.mean(each_y)) 
            each_y_std=np.max(np.abs(each_y))
            if each_y_std == 0:
                each_y = each_y + 50
            else:   
                each_y = each_y / each_y_std * 50 + 50

            canvas = np.zeros((100, 100, 3), dtype="uint8")
            for j in range(7):
                cv2.line(canvas, (int(each_x[j]), int(100 - each_y[j])), (int(each_x[j + 1]), int(100 - each_y[j + 1])), (255, 255, 255), thickness=4)
            self.get_gray(canvas,X_img)
        
        return X_img
        
    def get_gray(self,canvas,X_img):
        tempimg = cv2.resize(canvas,(20,20),cv2.INTER_LINEAR)
        img_Guassian = cv2.GaussianBlur(tempimg,(3,3),0.75)
        img_center = np.pad(img_Guassian, ((4, 4), (4, 4),(0,0)), 'constant')
        img_gray = cv2.cvtColor(img_center, cv2.COLOR_BGR2GRAY)
        X_img.append(img_gray)
        # cv2.imwrite('test.png', img_gray)

    #加载模型
    def loadModel(self,metaPath, ckptPath):
        sess=tf.Session()
        new_saver = tf.train.import_meta_graph(metaPath)
        sess.run(tf.global_variables_initializer())  
        new_saver.restore(sess, tf.train.latest_checkpoint(ckptPath))
        graph = tf.get_default_graph()
        return graph,sess

        # train_writer = tf.summary.FileWriter(ckptPath)
        # train_writer.add_graph(tf.get_default_graph())
