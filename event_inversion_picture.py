"""
    file name :event_inversion_picture.py
    Program IDE:PyCharm
    Create file data:2022/9/9 21:25
    File create by Author:lishiming
"""

import matplotlib.pyplot as plt
import matplotlib.image as mmg
import h5py
import numpy as np
import os
import cv2
import pandas

def findcircles(img):
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,param1=60,param2=150,minRadius=50,maxRadius=350)
    if circles is None:
        return None,None,None
    circles = np.uint16(np.around(circles))[0]
    for circle in circles:
        y,x,r = circle[0],circle[1],circle[2]
        if r>320 and y>=r and y+r<800 and x>=r and x+r<1280:
            # for i in range(30):
            #     for j in range(30):
            #         img[circle[1]-15+i][circle[0][0]-15+j] = 1
            return y,x,r
    return None,None,None

def get_imges(index):
    key = 'events'
    keys=['xs','ys','event_gs','ts']
    name = format(index,'03')
    datas = dict()
    with h5py.File('dataset\\train\\data\\'+name+'.h5',"r") as f:
        for index in range(4):
            datas[index]=f[key][keys[index]][:]
    length = datas[0].shape[0]
    size = (1280,800)
    frames_size = 150000
    root_pic = 'picture'+'\\'+name
    root_label = 'labels'+'\\'+name
    if not os.path.exists(root_pic):
        os.makedirs(root_pic)
    if not os.path.exists(root_label):
        os.makedirs(root_label)
    count_img = np.zeros(size,dtype=np.uint16)
    img = np.zeros(size,dtype=np.uint8)
    #cou = np.zeros((700,700),dtype=np.uint8)
    k=0
    for j in range(frames_size):
        count_img[datas[0][j]][datas[1][j]]+=1
        if img[datas[0][j]][datas[1][j]]<datas[2][j]/16:
            img[datas[0][j]][datas[1][j]] = datas[2][j]/16
    max_value = np.max(count_img)
    countimg = np.uint8(count_img*255/max_value)
    count_img = count_img>>1 + img>>1
    y,x,r = findcircles(countimg)
    if y!=None or x!=None:
        # cou[:,:]=0
        # cou[350-r:350+r,350-r:350+r] = countimg[x-r:x+r,y-r:y+r]
        # data1 = pandas.DataFrame(cou)
        # data1 = data1.to_csv(root+'\\'+str(k)+'.csv')
        mmg.imsave(root_pic+'\\'+str(k)+'.jpg',countimg)
        data = pandas.DataFrame([k,x,y,r])
        data.to_csv(root_label+'\\'+str(k)+'.csv')
        k = k+1
        if k%8==0:
            print(k)
    i=0
    while(i+frames_size+frames_size<length):
        count_img[:,:]=0
        img[:,:]=0
        for j in range(frames_size):
            count_img[datas[0][i+frames_size+j]][datas[1][i+frames_size+j]] +=1 #datas[2][i+frames_szie+j]/4095.0
            if img[datas[0][i+frames_size+j]][datas[1][i+frames_size+j]]<datas[2][i+frames_size+j]/16:
                img[datas[0][i+frames_size+j]][datas[1][i+frames_size+j]] = datas[2][i+frames_size+j]/16
        max_value = np.max(count_img)
        countimg = np.uint8(count_img*255/max_value)
        count_img = count_img>>1 + img>>1
        y,x,r = findcircles(countimg)
        if y!=None or x!=None:
            # cou[:,:]=0
            # cou[350-r:350+r,350-r:350+r] = countimg[x-r:x+r,y-r:y+r]
            # data1 = pandas.DataFrame(cou)
            # data1 = data1.to_csv(root+'\\'+str(k)+'.csv')
            # countimg[x-10:x+10,y-10:y+10]=255
            mmg.imsave(root_pic+'\\'+str(k)+'.jpg',countimg)
            data = pandas.DataFrame([k,x,y,r])
            data.to_csv(root_label+'\\'+str(k)+'.csv')
            k = k+1
            if k%8==0:
                print(k)
        i = i+frames_size

if __name__=='__main__':
    for i in range(1,121,5):
        print('数据集:'+str(i))
        get_imges(i)
#     get_imges(3)

