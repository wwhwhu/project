import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from deal.algo1 import cal1
from deal.draw_3d import draw3d
from deal.foredeal import img_maker, get_example_data

data, gt = get_example_data()
data2 = data
# 输出两百张图片在一起的原始3d图像
# draw3d("result\\init\\", "..\\result\\3d\\", title="原始数据", n=200)
for i in range(200):
    # 特征选择前的灰度图像
    print("正在预处理第{}张图片，请稍候".format(i))
    data2['indian_pines_corrected'][:, :, i] = img_maker(data['indian_pines_corrected'][:, :, i], i, save=True, plot=False)
# 输出两百张图片在一起的预处理后3d图像
# draw3d("result\\fore\\", "..\\result\\3d\\", title="预处理后的数据", n=200)
