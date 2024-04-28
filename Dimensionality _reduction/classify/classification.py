import numpy as np
import sklearn.svm as svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn import preprocessing
from deal.foredeal import get_example_data, img_maker
from sklearn import metrics
import warnings
warnings.filterwarnings("ignore")

data, gt = get_example_data()
gt_1 = gt['indian_pines_gt'].reshape(145 * 145, 1)
data2 = data
for i in range(200):
    data2['indian_pines_corrected'][:, :, i] = img_maker(data['indian_pines_corrected'][:, :, i], i, save=True,
                                                         plot=False)
min_max_scaler = preprocessing.MinMaxScaler()
data = min_max_scaler.fit_transform(data['indian_pines_corrected'].reshape((145*145, 200)))  # 归一化数据
print(data.shape)
data2 = min_max_scaler.fit_transform(data2['indian_pines_corrected'].reshape((145*145, 200)))  # 归一化数据
print(data2.shape)

res = [
    [90, 148, 56, 0, 199],
    [86, 0, 89, 74, 107],
    [56, 199, 0, 148, 88],
    [153, 60, 56, 199, 0],
]

data_algo1 = [data2[:, i] for i in res[0]]
data_algo1 = np.array(data_algo1).T
data_algo2 = [data2[i] for i in res[1]]
data_algo2 = np.array(data_algo1)
data_algo3 = [data2[i] for i in res[2]]
data_algo3 = np.array(data_algo1)
data_algo4 = [data2[i] for i in res[3]]
data_algo4 = np.array(data_algo1)
print(data_algo1.shape)

# 使用SVM进行分类
def svm_classify(data, label):
    x_train, x_test, y_train, y_test = train_test_split(data, label, test_size=0.3)
    svm_model = svm.SVC(kernel='poly', decision_function_shape='ovo')
    svm_model.fit(x_train, y_train)
    svm_model.fit(x_test, y_test)
    # 使用模型对测试集进行预测
    y_pred = svm_model.predict(x_test)
    # 计算并返回F1得分
    f1 = f1_score(y_test, y_pred, average='weighted')  # 'weighted'可根据类别不平衡情况进行调整
    print("F1得分：", f1)
    # y_pred = svm_model.predict(x_test)
    # print("测试集：\n", metrics.classification_report(y_test, y_pred))
    # print("测试集混淆矩阵：\n", metrics.confusion_matrix(y_test, y_pred))
    # y_pred_train = svm_model.predict(x_train)
    # print("训练集：\n", metrics.classification_report(y_train, y_pred_train))
    # print("训练集混淆矩阵：\n", metrics.confusion_matrix(y_train, y_pred_train))


# 原始数据分类
print("原始数据分类：")
svm_classify(data, gt_1.ravel())

# 预处理后的数据分类
print("预处理后的数据分类：")
svm_classify(data2, gt_1.ravel())

# 算法一的数据分类
print("算法一的数据分类：")
svm_classify(data_algo1, gt_1.ravel())

# 算法二的数据分类
print("算法二的数据分类：")
svm_classify(data_algo2, gt_1.ravel())

# 算法三的数据分类
print("算法三的数据分类：")
svm_classify(data_algo3, gt_1.ravel())

# 算法四的数据分类
print("算法四的数据分类：")
svm_classify(data_algo4, gt_1.ravel())
