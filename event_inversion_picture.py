"""
    file name :event_inversion_picture.py
    Program IDE:PyCharm
    Create file data:2022/9/9 21:25
    File create by Author:lishiming
"""

import matplotlib.image as mmg
import h5py
import numpy as np
import os
import cv2
import pandas
from setting import dataset_root, event, event_e, size, frames_size, picture_save_dir, label_save_dir


#寻找圆心
def find_circles(img):
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 50, param1=60, param2=150, minRadius=50, maxRadius=350)
    if circles is None:
        return None, None, None
    circles = np.uint16(np.around(circles))[0]
    for circle in circles:
        y, x, r = circle[0], circle[1], circle[2]
        if r > 320 and y >= r and y + r < 800 and x >= r and x + r < 1280:
            # for i in range(30):
            #     for j in range(30):
            #         img[circle[1]-15+i][circle[0][0]-15+j] = 1
            return y, x, r
    return None, None, None


# 创建存储文件夹
def create_file(name):
    root_pic = os.path.join(picture_save_dir, name)
    root_label = os.path.join(label_save_dir, name)
    if not os.path.exists(root_pic):
        os.makedirs(root_pic)
    if not os.path.exists(root_label):
        os.makedirs(root_label)


# 获取文件地址
def get_dir():
    pass


# h5文件打开以及存储事件流
def event_save(index):
    name = format(index, '03')
    datas = []
    with h5py.File(dataset_root + name + '.h5', "r") as f:
        for i in range(4):
            datas[i] = f[event][event_e[i]][:]

    return datas, name


# 事件流转化为矩阵
def event_to_matrix(datas):
    count_img = np.zeros(size, dtype=np.uint16)
    img = np.zeros(size, dtype=np.uint8)
    for j in range(frames_size):
        count_img[datas[0][j]][datas[1][j]] += 1
        if img[datas[0][j]][datas[1][j]] < datas[2][j] / 16:
            img[datas[0][j]][datas[1][j]] = datas[2][j] / 16
    max_value = np.max(count_img)
    countimg = np.uint8(count_img * 255 / max_value)
    count_img = count_img >> 1 + img >> 1
    return img, countimg, count_img


def get_imges(index):
    datas, name = event_save(index=index)

    length = datas[0].shape[0]

    create_file(name)  # 创建文件夹

    img, countimg, count_img = event_to_matrix(datas)  # event转化为matrix

    y, x, r = find_circles(countimg)

    k = 0
    if y or x:
        mmg.imsave(picture_save_dir + '\\' + str(k) + '.jpg', countimg)
        data = pandas.DataFrame([k, x, y, r])
        data.to_csv(label_save_dir + '\\' + str(k) + '.csv')
        k = k + 1
        if k % 8 == 0:
            print(k)

    i = 0
    while (i + frames_size * 2 < length):
        count_img[:, :] = 0
        img[:, :] = 0
        for j in range(frames_size):
            count_img[datas[0][i + frames_size + j]][
                datas[1][i + frames_size + j]] += 1  # datas[2][i+frames_szie+j]/4095.0
            if img[datas[0][i + frames_size + j]][datas[1][i + frames_size + j]] < datas[2][i + frames_size + j] / 16:
                img[datas[0][i + frames_size + j]][datas[1][i + frames_size + j]] = datas[2][i + frames_size + j] / 16
        max_value = np.max(count_img)
        countimg = np.uint8(count_img * 255 / max_value)
        count_img = count_img >> 1 + img >> 1
        y, x, r = find_circles(countimg)
        if y != None or x != None:
            mmg.imsave(picture_save_dir + '\\' + str(k) + '.jpg', countimg)
            data = pandas.DataFrame([k, x, y, r])
            data.to_csv(label_save_dir + '\\' + str(k) + '.csv')
            k = k + 1
            if k % 8 == 0:
                print(k)
        i = i + frames_size


if __name__ == '__main__':
    for i in range(1, 121, 5):
        print('数据集:' + str(i))
        get_imges(i)