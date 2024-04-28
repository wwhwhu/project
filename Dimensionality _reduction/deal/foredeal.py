import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from sklearn.ensemble import IsolationForest
import scipy.io as scio


# 读取Example数据
def get_example_data():
    dataFile = 'dataset\\Indian_Pines\\example\\Indian_pines_corrected.mat'
    dataGt = 'dataset\\Indian_Pines\\example\\Indian_pines_gt.mat'
    data = scio.loadmat(dataFile)
    gt = scio.loadmat(dataGt)

    # 查看data与gt的shape以及keys
    print("data keys: ", data.keys(), "data shape: ", (data['indian_pines_corrected']).shape)
    print("gt keys: ", gt.keys(), "gt shape: ", (gt['indian_pines_gt']).shape)

    data_1 = data['indian_pines_corrected'].reshape((145 * 145, 200))
    gt_1 = gt['indian_pines_gt'].reshape(145 * 145, 1)

    # 查看data_1与gt_1的shape
    print("data_1 shape: ", data_1.shape)
    print("gt_1 shape: ", gt_1.shape)
    return data, gt


# 预处理函数
def img_maker(data_img2, i, save=False, plot=False):
    # 去噪 - 高斯滤波
    data_img = cv2.GaussianBlur(data_img2, (3, 3), 0)

    # 归一化 - 最小-最大归一化
    x_min = np.min(data_img)
    x_max = np.max(data_img)
    data_img = (data_img - x_min) / (x_max - x_min)

    # 异常值检测 - Isolation Forest
    clf = IsolationForest(contamination=0.05)  # 设置异常值比例为5%
    clf.fit(data_img)
    # outliers中-1表示异常值，1表示正常值
    outliers = clf.predict(data_img)

    # 异常值填充使用线性插值填充
    outlier_indices = np.where(outliers == -1)[0]

    # 进行插值前，确保data_img是一维数组
    if data_img.ndim > 1:
        data_img = data_img.flatten()

    # 创建一个线性插值模型，仅使用正常值
    interp = interp1d(
        x=np.delete(np.arange(len(data_img)), outlier_indices),
        y=np.delete(data_img, outlier_indices),
        kind='linear',
        fill_value='extrapolate'  # 用于填充超出数据范围的异常值
    )

    # 使用插值模型填充异常值
    data_img[outlier_indices] = interp(outlier_indices)
    # reshape回原来的形状
    data_img = data_img.reshape(145, 145)
    if save:
        plt.imsave('result\\init\\' + str(i) + '.png', data_img2, cmap='gray')
        plt.imsave('result\\fore\\' + str(i) + '.png', data_img, cmap='gray')
    if plot:
        plt.text(x=0, y=15, s=i, fontdict=dict(fontsize=30, color='r'))
        plt.ion()
        plt.imshow(data_img, cmap='gray')
        plt.axis('off')
        plt.ioff()
        plt.pause(0.05)
        plt.clf()
    return data_img

