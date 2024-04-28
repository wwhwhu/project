import os
from mayavi import mlab

import cv2
import numpy as np
from matplotlib import pyplot as plt, image as mpimg

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']


def draw3d(path, save_path, title, n):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # 选择要显示的图片索引
    # indices = [0, 5, 10]  # 例如，你想显示第1、6、11张图片
    indices = range(n)
    # 对每张图片进行绘制
    for i, index in enumerate(indices):
        # 提取单个图片
        image = mpimg.imread(os.path.join(path, f"{index}.png"))
        print(f"add pic{i}")
        # 计算图片的坐标
        X, Y = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
        Z = np.full_like(X, i)  # 在Z轴上放置图片
        # 绘制图片
        ax.plot_surface(X, -Z, Y, rstride=1, cstride=1, facecolors=image)
    ax.set_xlabel('width')
    ax.set_ylabel('num')
    ax.set_zlabel('height')
    ax.set_title(title)
    # 保存图片
    plt.savefig(save_path + f"{title}.png")
    plt.axis('off')
    plt.ioff()
    plt.pause(0.05)
    plt.clf()
