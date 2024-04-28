import numpy as np
import scipy.io
from sklearn.decomposition import PCA
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from scipy import signal
from multiprocessing import Pool

# VMD算法已经以库函数形式实现
from vmdpy import VMD


# 数据采集，此处为示例
def collect_data():
    # 读取data文件夹下mat文件
    data2 = scipy.io.loadmat("data/shachen.mat")
    print("数据采集完成", '\n雨天：\n', data2.keys())
    print("数据雨天：", data2['X'].shape, data2['X'].dtype, '内容：\n', data2['X'])
    return data2['X'].flatten()


# 多尺度分解
# 参数说明：
# signal: 输入信号，alpha: 正则化参数，tau: 信号的时间间隔，K: 分解的尺度数，DC: 是否保留直流分量，init: 初始化方式，tol: 收敛阈值
# 返回值：
# u: 分解后的信号
def vmd_decomposition(signal):
    print("VMD分解中...")
    u, _, _ = VMD(signal, alpha=4000, tau=0.0, K=16, DC=0, init=1, tol=1e-7)
    print("VMD分解完成", u.shape, u.dtype, u)
    return u


# RBF建模
def rbf_modeling(low_freq_components, subsample_factor=1):
    print("RBF建模中...")
    kernel = RBF(length_scale=1.0)
    gp = GaussianProcessRegressor(kernel=kernel)

    # 对数据进行降采样
    if subsample_factor > 1:
        indices = np.arange(0, low_freq_components.size, subsample_factor)
        low_freq_components_subsample = low_freq_components[indices]
        x_subsample = np.arange(low_freq_components_subsample.size).reshape(-1, 1)
        gp.fit(x_subsample, low_freq_components_subsample)
    else:
        gp.fit(np.arange(low_freq_components.size).reshape(-1, 1), low_freq_components)
    print("RBF建模完成", gp)
    return gp


# PCA去噪
def pca_noise_removal(high_freq_components):
    print("PCA去噪中...")
    pca = PCA(n_components=0.95)  # 保留95%的方差
    principal_components = pca.fit_transform(high_freq_components)
    print("PCA去噪完成", principal_components.shape, principal_components.dtype, principal_components)
    return principal_components


# 并行处理PCA降噪后的数据
def parallel_processing_post_pca(data_chunk):
    # 假设对PCA处理后的数据进行某种形式的处理，此处为示例
    print("并行处理中...")
    processed_data = np.mean(data_chunk, axis=0)  # 示例处理：计算均值
    print("并行处理完成", processed_data.shape, processed_data.dtype, processed_data)
    return processed_data


def main():
    # 采集数据
    data = collect_data()
    # 不拆分原始数据，而是首先进行VMD分解和PCA降噪
    decomposed = vmd_decomposition(data)
    low_freq, high_freq = decomposed[0], decomposed[1:]
    # 对低频分量进行RBF建模, subsample_factor=1表示不降采样
    model = rbf_modeling(low_freq, subsample_factor=1)
    noise_removed = pca_noise_removal(high_freq)
    # 假设noise_removed是一个大型多维数据集，需要进一步并行处理
    # 这里以均匀分割noise_removed为例，演示并行处理
    chunks = np.array_split(noise_removed, 15)  # 假设我们将数据分为15块进行并行处理
    with Pool(15) as p:
        results = p.map(parallel_processing_post_pca, chunks)
    print("15线程并行处理结果：", results)
    # results 保存了所有并行处理结果


if __name__ == "__main__":
    main()
