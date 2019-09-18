# 使用goodFeaturesToTrack函数检测角点
import cv2
import numpy as np
import math
import csv
import matplotlib.pyplot as plot
import PIL
import io


class HandDetect:
    #def __init__(self):
        

    # 寻找所有直线端点（包括角点和原本的直线端点）
    def find_possible_point(self, key_points, cdt_data):
        point_list = []  # 用来存放角点以及线段的端点
        for i in range(len(cdt_data)):
            if cdt_data[i] not in point_list:
                if (i - 1) >= 0 and cdt_data[i - 1] == (-1, -1) and cdt_data[i+1] != (-1, -1) and (i+1) < len(cdt_data):
                    point_list.append(cdt_data[i])
                elif (i - 1) >= 0 and cdt_data[i - 1] == (-1, -1) and cdt_data[i+1] == (-1, -1) and (i+1) < len(cdt_data):
                    point_list.append(cdt_data[i])
                    point_list.append((-1, -1))
                elif cdt_data[i] in key_points and cdt_data[i + 1] != (-1, -1) and (i + 1 < len(cdt_data)):
                    point_list.append(cdt_data[i])
                elif cdt_data[i] in key_points and cdt_data[i + 1] == (-1, -1) and (i + 1 < len(cdt_data)):
                    point_list.append(cdt_data[i])
                    point_list.append((-1, -1))
                elif (i + 1) < len(cdt_data) and cdt_data[i + 1] == (-1, -1) and (cdt_data[i] not in key_points):
                    point_list.append(cdt_data[i])
                    point_list.append((-1, -1))
        return point_list

    # 将散点拟合成直线然后求出三个点
    def detect_line(self, key_points, cdt_data):
        point_list = self.find_possible_point(key_points, cdt_data)
        # 找出最长的线
        max_index = 0
        max_distance = 0
        for j in range(len(point_list)):
            if (j+1) < len(point_list) and point_list[j+1] != (-1, -1) and point_list[j] != (-1, -1):
                if max_distance < math.sqrt((point_list[j][0] - point_list[j+1][0]) ** 2
                                            + (point_list[j][1] - point_list[j+1][1]) ** 2):
                    max_distance = math.sqrt((point_list[j][0] - point_list[j+1][0]) ** 2
                                             + (point_list[j][1] - point_list[j+1][1]) ** 2)
                    max_index = j
        max_start = point_list[max_index]
        max_end = point_list[max_index + 1]

        # 找出次最长的线
        sec_max_distance = 0
        sec_max_index = 0
        for m in range(len(point_list)):
            if (m+1) < len(point_list) and point_list[m+1] != (-1, -1) and point_list[m] != (-1, -1):
                distance = math.sqrt((point_list[m][0] - point_list[m+1][0]) ** 2
                                     + (point_list[m][1] - point_list[m+1][1]) ** 2)
                if (sec_max_distance < distance) and (distance < max_distance):
                    sec_max_distance = distance
                    sec_max_index = m

        sec_max_start = point_list[sec_max_index]
        sec_max_end = point_list[sec_max_index + 1]

        max_start_index = cdt_data.index(max_start)
        max_end_index = cdt_data.index(max_end)
        sec_max_start_index = cdt_data.index(sec_max_start)
        sec_max_end_index = cdt_data.index(sec_max_end)

        max_line = np.array(cdt_data[max_start_index: max_end_index+1])  # 要拟合的最长的线的点集
        sec_max_line = np.array(cdt_data[sec_max_start_index: sec_max_end_index+1])  # 要拟合的次最长线的点集

        max = cv2.fitLine(max_line, cv2.DIST_HUBER, 0, 0.01, 0.01)
        max = np.reshape(max, 4)
        max = max.tolist()
        sec_max = cv2.fitLine(sec_max_line, cv2.DIST_HUBER, 0, 0.01, 0.01)
        sec_max = (np.reshape(sec_max, 4)).tolist()

        # 求交点
        k1 = float(max[1] / max[0])
        k2 = float(sec_max[1] / sec_max[0])
        cross_point_x = (sec_max[3] - max[3] + k1 * max[2] - k2 * sec_max[2]) / (k1 - k2)
        cross_point_y = k1 * cross_point_x - k1 * max[2] + max[3]

        if ((max_start[0] - cross_point_x) ** 2 + (max_start[1] - cross_point_y) ** 2) > \
                ((max_end[0] - cross_point_x) ** 2 + (max_end[1] - cross_point_y) ** 2):
            point1 = max_start
        else:
            point1 = max_end

        if ((sec_max_start[0] - cross_point_x) ** 2 + (sec_max_start[1] - cross_point_y) ** 2) > \
                ((sec_max_end[0] - cross_point_x) ** 2 + (sec_max_end[1] - cross_point_y) ** 2):
            point2 = sec_max_start
        else:
            point2 = sec_max_end

        point3 = (cross_point_x, cross_point_y)

        return point1, point2, point3

    def take_first(self, elem):  # 用来排序用的[(2, 3), (4, 3), (5, 9)]按元祖的第一个元素进行排序
        return elem[0]

    def detect_key_point(self, cdt_data, image):  # 选择关键点
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 由于Shi-Tomasi算子需要float32的输入图像，因此转换一下数据格式
        gray = np.float32(gray)
        key_points = []  # 用来存放关键点
        kp = cv2.goodFeaturesToTrack(gray, 12, 0.04, 0)  # 返回的点是x, y两列
        if kp is not None and len(kp) > 0:
            for x, y in np.float32(kp).reshape(-1, 2):
                key_points.append((x, y))
        cdt_data = self.get_correct_list(cdt_data)
        del_data = []
        for i in cdt_data:
            if not i in del_data and i != (-1, -1):
                del_data.append(i)
            elif i == (-1, -1):
                del_data.append(i)
        cdt_data = del_data
        n_index = 0
        near_index = []  # 用来存放离角点最近的点在cdt_data中的索引
        for i in range(len(key_points)):
            min_distance = 100000000
            for j in range(len(cdt_data)):
                if cdt_data[j] != (-1, -1):
                    if min_distance > (math.sqrt((key_points[i][0]-cdt_data[j][0])**2
                                                 + (key_points[i][1]-cdt_data[j][1]) ** 2)):
                        min_distance = (math.sqrt((key_points[i][0]-cdt_data[j][0])**2
                                                  + (key_points[i][1] - cdt_data[j][1])**2))
                        n_index = j
            near_index.append(n_index)

        order_point = []
        for k in range(len(key_points)):
            order_point.append((near_index[k], key_points[k]))
        order_point.sort(key=self.take_first)

        # 将角点插入到cdt_data中
        for m in range(len(order_point)):
            cdt_data.insert((order_point[m][0] + m), order_point[m][1])  # 将角点插入cdt_data中,记得插入后列表长度会变长，所以要加上索引

        key_points = []
        for n in range(len(order_point)):
            key_points.append(order_point[n][1])

        point1, point2, point3 = self.detect_line(key_points, cdt_data)  # 返回三个点

        return point1, point2, point3

    def coordinate_to_picture(self, cdt_data):
        cdt_data = [[float(x) for x in row] for row in cdt_data]  # 将数据从string形式转化为float
        x_list_total = []
        y_list_total = []
        # 创建图并命名
        plot.figure('Line fig')
        ax = plot.gca()
        # 将坐标原点放到左上角
        ax.xaxis.tick_top()
        ax.invert_yaxis()
        plot.subplots_adjust(left=0, right=1, top=1, bottom=0)  # 将坐标轴设置为距离边缘无margin
        plot.axis([0, 400, 400, 0])  # 设置窗口大小为 400 * 400
        for i in cdt_data:
            if i != [-1, 11, -1]:
                x_list_total.append(i[0])
                y_list_total.append(i[1])
            elif i == [-1, 11, -1]:
                ax.plot(x_list_total, y_list_total, color='#000000')
                x_list_total = []
                y_list_total = []

        plot.axis('off')  # 关掉坐标轴
        fig = plot.gcf()
        fig.set_size_inches(4, 4)  # 设置图片的尺寸为400 * 400
        # 申请缓存
        self.buffer_ = io.BytesIO()
        fig.savefig(self.buffer_, format="jpg")
        self.buffer_.seek(0)
        image = PIL.Image.open(self.buffer_)
        img_mat = np.asarray(image)
        self.buffer_.close()
        plot.close('all')  # 必须加上，否则所有对图片的操作都会累计起来
        return img_mat  # 自行修改存放图片的位置

    # 参数为np.array.shape为(-, 3)
    def get_correct_list(self, cdt_data):
        data = []
        cdt_data = [[float(x) for x in row] for row in cdt_data]  # 将数据从string形式转化为float
        for row in cdt_data:  # 将csv文件中的数据保存到cdt_data中
            if row[0] == -1:
                data.append((-1, -1))
            else:
                data.append((row[0], row[1]))
        return data  # 返回一个正常的点集列表

    def hand_detect(self, cdt_data):
        image = self.coordinate_to_picture(cdt_data)
        point1, point2, point3 = self.detect_key_point(cdt_data, image)
        return point1, point2, point3