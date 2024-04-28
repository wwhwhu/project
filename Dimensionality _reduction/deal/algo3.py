import numpy as np
import random
from PIL import Image
from skimage.metrics import structural_similarity as compare_ssim
from skimage.io import imread
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr


# 假设图片被编号为0到199
from deal.draw_3d import draw3d

image_indices = list(range(200))
best_fitness_list = []


# 一个函数用于计算两张图片的区块相似度
def calculate_similarity(image1_idx, image2_idx):
    # 读取两个图像
    imageA = imread(f'../result/fore/{image1_idx}.png', as_gray=True)
    imageB = imread(f'../result/fore/{image2_idx}.png', as_gray=True)
    # 计算MSSIM
    ssim, _ = compare_ssim(imageA, imageB, full=True)
    # print(f"图片{image1_idx}和图片{image2_idx}的MSSIM值为{ssim}")
    return ssim


# 适应度函数, chromosome是一个图片索引的列表
def fitness_function(chromosome):
    similarity_sum = 0
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            similarity_sum += calculate_similarity(chromosome[i], chromosome[j])
    # 适应度是相似度之和的倒数值，因为我们想要相似度尽可能小
    return 1/similarity_sum


# 差分进化算法中的变异操作
def mutate(target_idx, population, F):
    # 随机选择三个不等于target_idx的索引
    indices = list(range(len(population)))
    indices.remove(target_idx)
    random_indices = np.random.choice(indices, 3, replace=False)
    a, b, c = population[random_indices[0]], population[random_indices[1]], population[random_indices[2]]
    # 将列表转换为Numpy数组进行逐元素操作
    mutant_vector = np.clip(a + F * (np.array(b) - np.array(c)), 0, 199)  # 确保索引在有效范围内
    return mutant_vector.astype(int)  # 确保索引为整数


# 差分进化算法中的交叉操作
def crossover(mutant_vector, target_vector, CR):
    cross_points = np.random.rand(len(target_vector)) < CR
    # 如果没有交叉点，则至少选择一个点进行交叉
    if not np.any(cross_points):
        cross_points[np.random.randint(0, len(target_vector))] = True
    trial_vector = np.where(cross_points, mutant_vector, target_vector)
    return trial_vector


# 差分进化算法
def differential_evolution(pop_size, gene_pool, chromosome_length, generations, F, CR):
    # 初始化种群
    population = [[random.choice(gene_pool) for _ in range(chromosome_length)] for _ in range(pop_size)]
    fitness_scores = [fitness_function(ch) for ch in population]

    for g in range(generations):
        for i in range(pop_size):
            # 变异
            mutant_vector = mutate(i, population, F)
            # 交叉
            trial_vector = crossover(mutant_vector, population[i], CR)
            # 选择
            if fitness_function(trial_vector) > fitness_scores[i]:
                population[i] = trial_vector
                fitness_scores[i] = fitness_function(trial_vector)

        print(f'Generation {g} - Fitness_scores: {fitness_scores}')
        print(f'Generation {g} - Best fitness: {max(fitness_scores)}')
        best_fitness_list.append(max(fitness_scores))

    # 绘制best_fitness_list的折线图
    plt.plot(best_fitness_list)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness(1/similarity)')
    plt.savefig('../result/after/3/best_fitness_train.png')
    plt.show()

    # 返回最优的个体
    best_fitness = max(fitness_scores)
    best_chromosome = population[fitness_scores.index(best_fitness)]
    return best_chromosome


def run_algo3():
    best_solution = differential_evolution(
        pop_size=200,
        gene_pool=image_indices,
        chromosome_length=5,
        generations=100,
        F=0.8,  # 差分权重
        CR=0.9  # 交叉概率
    )
    # result: [153, 60, 56, 199, 0] best fitness: 0.5691355456851476
    print("Best solution (image indices):", best_solution)
    res = []
    for i in best_solution:
        # 打开图片
        image = Image.open(f"../result/fore/{i}.png")
        # 将图片转换为numpy数组
        image_array = np.array(image)
        # 将图片数组添加到res列表中
        res.append(image_array)
    return res


def cal3():
    # 计算data_after_deal的5个维度图片相似性
    correlation_matrix = np.zeros((5, 5))
    data_after_deal = run_algo3()
    print(data_after_deal)
    for i in range(5):
        for j in range(5):
            # 计算第i张图片和第j张图片之间的皮尔逊相关系数
            correlation, _ = pearsonr(data_after_deal[i].flatten(), data_after_deal[j].flatten())
            correlation_matrix[i, j] = correlation
    # 输出关联性矩阵
    print("关联性矩阵：")
    print(correlation_matrix)

    # 绘制热图
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', square=True)
    plt.title("DE降维关联性矩阵")
    plt.xlabel("图片编号")
    plt.ylabel("图片编号")
    plt.savefig("..\\result\\after\\3\\algo3.png")
    plt.show()

    for i in range(5):
        plt.text(x=0, y=15, s=i, fontdict=dict(fontsize=30, color='r'))
        plt.imshow(data_after_deal[i], cmap='gray')
        plt.savefig(f'..\\result\\after\\3\\{i}.png')
        plt.show()

    # 输出5张图片在一起的3d图像
    draw3d("..\\result\\after\\3\\", "..\\result\\after\\3\\", title="算法3降维后", n=5)

