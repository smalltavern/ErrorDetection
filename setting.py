"""
    file name :setting.py
    Program IDE:PyCharm
    Create file data:2022/9/10 14:51
    File create by Author:lishiming
"""

# 数据集的相关路径
dataset_root = 'dataset\\train\\data\\'
label_root = 'labels'

frames_size = 150000

size = (1280, 800)

event = 'event'  # 数据集中的事件
event_e = ['xs', 'ys', 'event_gs', 'ts']  # 事件流e的存储信息

picture_save_dir = 'picture'  # 图片信息的存储路径
label_save_dir = 'label'