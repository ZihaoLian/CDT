import numpy as np
import lime.lime_tabular
from cdt_util import dcmp
import lime

class Explanation:
    def __init__(self):
        #如果要换其他模型，将下面的改成该模型实际训练用的数据
        cdt_feature=np.loadtxt("./cdt_feature.csv",delimiter=",",skiprows=0)
        self.explainer = lime.lime_tabular.LimeTabularExplainer(cdt_feature[:,:408], feature_names=[i for i in range(408)], class_names=["0","1"], discretize_continuous=True)
        self.level_explanation=["个别","部分","大部分"]
        self.negative_explanation=[["数字不规整","数字绘画时间过长或过短","数字空间分布有误","数字重复","数字缺失","没有首先画了数字12，3，6，9"],
                                ["钟表外圈间断过多","钟表外圈形状不规则","钟表外圈没有闭合"],
                                ["绘画指针过程钟思考时间过长","指针位置错误","时针分针长度差异有误"],
                                ["绘画时间过长","实验时间过长","思考时间过长","存在无意义笔画"]]
        self.positive_explanation=[["数字规整","数字绘画时间合适","数字空间分布合理","数字无重复","数字无缺失","首先画了数字12，3，6，9"],
                                ["钟表外圈连贯","钟表外圈形状规则","钟表外圈闭合"],
                                ["绘画指针过程钟思考时间恰当","指针位置准确","时针分针长度差异明显"],
                                ["绘画时间在合理范围内","实验时间在合理范围内","思考时间恰当","无意义笔画较少"]]   
        #每个特征对应的解释，建议最好别动，只动上面的文字                     
        self.code=[
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            13,14,13,14,13,14,13,14,13,14,13,14,13,14,13,14,13,14,13,14,
            13,14,10,10,11,11,10,10,10,15,
            20,21,21,21,21,21,21,22,22,
            30,31,31,32,
            43,43,40,40,41,42,42,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            10,10,11,11,10,10,10,12,12,12,
            13,14,13,14,13,14,13,14,13,14,13,14,13,14,13,14,13,14,13,14,
            13,14,10,10,11,11,10,10,10,15,
            20,21,21,21,21,21,21,22,22,
            30,31,31,32,
            43,43,40,40,41,42,42,
            13,14,10,10,10,43,41,42]

    def explain(self,model,feature,explanation_max_num=40):
        feature=feature.reshape(408)
        #该函数的feature必须是一维的，有毒
        exp = self.explainer.explain_instance(feature,model.predict_proba, num_features=explanation_max_num,top_labels=1)
        exp_map=exp.as_map()
        #仅允许单个样例
        for label in exp_map.keys():
            return self.decode(exp_map[label],label)
        
    #将机器输出的作为判断依据的特征编译成人易懂概括性的语句
    def decode(self,model_explanation,label):
        #support 指支持模型分类， oppose指不支持模型分类
        support_code=np.zeros(4*6)
        oppose_code=np.zeros(4*6)
        support_counter=np.zeros(6)
        oppose_counter=np.zeros(6)

        for exp in model_explanation:
            exp_code=int(self.code[exp[0]])
            if dcmp(exp[1])>0:
                support_code[(int(exp_code/10)-1)*6+exp_code%10]+=exp[1]
                if exp_code/10==1:
                    support_counter[exp_code%10]+=1
            else:
                oppose_code[(int(exp_code/10)-1)*6+exp_code%10]-=exp[1]
                if exp_code/10==1:
                    oppose_counter[exp_code%10]+=1

        #选出影响分类的最大十个个要素
        max_support_indexs=(-support_code).argsort()[:10]
        max_oppose_indexs=(-oppose_code).argsort()[:10]
        support_explanation=[]
        oppose_explanation=[]
        for i in max_support_indexs:
            if support_code[i]>0:
                support_explanation.append(self.decode_helper(int(i/6),i%6,oppose_counter[i%6],label,0))
            else:
                break
        for i in max_oppose_indexs:
            if oppose_code[i]>0:
                oppose_explanation.append(self.decode_helper(int(i/6),i%6,oppose_counter[i%6],label^1,1))
            else:
                break
        return label,support_explanation,oppose_explanation

    #time 该特征不支持分类结果次数 tag>0正面评价
    def decode_helper(self,x,y,time,label,tag):
        explanation=""
        #数字类的解释加上程度作为修饰
        if x == 0 and y<5 :
            if tag>0:
                if time<7:
                    explanation+=self.level_explanation[0]
                elif time<15:
                    explanation+=self.level_explanation[1]
                else:
                    explanation+=self.level_explanation[2]
            else:
                if time<15:
                    explanation+=self.level_explanation[2]
        if label>0:
            explanation+=self.negative_explanation[x][y]
        else:
            explanation+=self.positive_explanation[x][y]
        return explanation



                



