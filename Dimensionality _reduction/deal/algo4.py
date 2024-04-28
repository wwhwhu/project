import numpy as np
import random
from PIL import Image
from scipy.stats import pearsonr
from skimage.metrics import structural_similarity as compare_ssim
from skimage.io import imread
import matplotlib.pyplot as plt
import seaborn as sns

from deal.draw_3d import draw3d

image_indices = list(range(200))
best_fitness_list = []


def calculate_similarity(image1_idx, image2_idx):
    imageA = imread(f'../result/fore/{image1_idx}.png', as_gray=True)
    imageB = imread(f'../result/fore/{image2_idx}.png', as_gray=True)
    ssim, _ = compare_ssim(imageA, imageB, full=True)
    return ssim


def fitness_function(chromosome):
    similarity_sum = 0
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            similarity_sum += calculate_similarity(chromosome[i], chromosome[j])
    return 1 / similarity_sum


def initialize_population(pop_size, gene_pool, chromosome_length):
    return [[random.choice(gene_pool) for _ in range(chromosome_length)] for _ in range(pop_size)]


def update_distribution(population, fitness_scores, gene_pool):
    # 基于优秀样本的参数估计
    top_samples = select_top_samples(population, fitness_scores)
    top_samples_flat = np.array(top_samples).flatten()
    distribution = [top_samples_flat.tolist().count(gene) / len(top_samples_flat) for gene in gene_pool]
    return distribution

def select_top_samples(population, fitness_scores, top_ratio=0.2):
    # 选择顶部个体
    sorted_indices = np.argsort(-np.array(fitness_scores))
    top_k = int(top_ratio * len(population))
    top_indices = sorted_indices[:top_k]
    return np.array(population)[top_indices]


def sample_from_distribution(distribution, gene_pool, chromosome_length, pop_size):
    # 从估计的分布中采样新个体
    new_population = []
    for _ in range(pop_size):
        chromosome = np.random.choice(gene_pool, size=chromosome_length, replace=True, p=distribution)
        new_population.append(list(chromosome))
    return new_population


def EDA(pop_size, gene_pool, chromosome_length, generations):
    population = initialize_population(pop_size, gene_pool, chromosome_length)
    fitness_scores = []
    for g in range(generations):
        fitness_scores = [fitness_function(ch) for ch in population]
        print(f'Generation {g} - Fitness_scores: {fitness_scores}')
        print(f'Generation {g} - Best fitness: {max(fitness_scores)}')
        best_fitness_list.append(max(fitness_scores))

        distribution = update_distribution(population, fitness_scores, gene_pool)
        population = sample_from_distribution(distribution, gene_pool, chromosome_length, pop_size)

    plt.plot(best_fitness_list)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness(1/similarity)')
    plt.savefig('../result/after/4/best_fitness_train.png')
    plt.show()
    best_fitness = max(fitness_scores)
    best_chromosome = population[fitness_scores.index(best_fitness)]
    return best_chromosome


def run_algo4():
    # 运行遗传算法， 种群大小：200， 基因池：image_indices， 染色体长度：5， 迭代次数：1000， 变异率：0.01
    best_solution = EDA(
        pop_size=200,
        gene_pool=image_indices,
        chromosome_length=5,
        generations=100
    )
    # result: [90, 148, 56, 0, 199] best fitness: 0.5495546710602692
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


def cal4():
    # 计算data_after_deal的5个维度图片相似性
    correlation_matrix = np.zeros((5, 5))
    data_after_deal = run_algo4()
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
    plt.title("EDA降维关联性矩阵")
    plt.xlabel("图片编号")
    plt.ylabel("图片编号")
    plt.savefig("..\\result\\after\\4\\algo4.png")
    plt.show()

    for i in range(5):
        plt.text(x=0, y=15, s=i, fontdict=dict(fontsize=30, color='r'))
        plt.imshow(data_after_deal[i], cmap='gray')
        plt.savefig(f'..\\result\\after\\4\\{i}.png')
        plt.show()

    # 输出5张图片在一起的3d图像
    draw3d("..\\result\\after\\4\\", "..\\result\\after\\4\\", title="算法4降维后", n=5)

