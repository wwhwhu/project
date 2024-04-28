# 基于遗传算法的特征选择（降维，20个维度选择5个进行分类）
import numpy as np
import random

# 假设图片被编号为0到199
from PIL import Image
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import pearsonr
from skimage.metrics import structural_similarity as compare_ssim
from skimage.io import imread
import numpy as np
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


# 初始化种群
def initialize_population(pop_size, gene_pool, chromosome_length):
    return [[random.choice(gene_pool) for _ in range(chromosome_length)] for _ in range(pop_size)]


# 选择函数
def selection(population, fitness_scores):
    # 这里使用简单的基于适应度比例的选择
    total_fitness = sum(fitness_scores)
    selection_probs = [f / total_fitness for f in fitness_scores]
    selected_indices = random.choices(range(len(population)), weights=selection_probs, k=len(population))
    return [population[i] for i in selected_indices]


# 交叉函数
def crossover(parent1, parent2):
    # 这里使用单点交叉
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


# 变异函数
def mutate(chromosome, gene_pool, mutation_rate):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = random.choice(gene_pool)
    return chromosome


# 遗传算法主函数
def genetic_algorithm(pop_size, gene_pool, chromosome_length, generations, mutation_rate):
    population = initialize_population(pop_size, gene_pool, chromosome_length)
    fitness_scores = []
    for g in range(generations):
        fitness_scores = [fitness_function(ch) for ch in population]
        print(f'Generation {g} - Fitness_scores: {fitness_scores}')
        print(f'Generation {g} - Best fitness: {max(fitness_scores)}')
        best_fitness_list.append(max(fitness_scores))
        population = selection(population, fitness_scores)

        # 生成下一代
        next_generation = []
        for i in range(0, len(population), 2):
            parent1, parent2 = population[i], population[i + 1]
            child1, child2 = crossover(parent1, parent2)
            next_generation.extend([mutate(child1, gene_pool, mutation_rate), mutate(child2, gene_pool, mutation_rate)])

        population = next_generation
    # 绘制best_fitness_list的折线图
    plt.plot(best_fitness_list)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness(1/similarity)')
    plt.savefig('../result/after/1/best_fitness_train.png')
    plt.show()
    # 最后返回最优的个体
    best_fitness = max(fitness_scores)
    best_chromosome = population[fitness_scores.index(best_fitness)]
    return best_chromosome


def run_algo1():
    # 运行遗传算法， 种群大小：200， 基因池：image_indices， 染色体长度：5， 迭代次数：1000， 变异率：0.01
    best_solution = genetic_algorithm(
        pop_size=200,
        gene_pool=image_indices,
        chromosome_length=5,
        generations=100,
        mutation_rate=0.01
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


def cal1():
    # 计算data_after_deal的5个维度图片相似性
    correlation_matrix = np.zeros((5, 5))
    data_after_deal = run_algo1()
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
    plt.title("GA降维关联性矩阵")
    plt.xlabel("图片编号")
    plt.ylabel("图片编号")
    plt.savefig("..\\result\\after\\1\\algo1.png")
    plt.show()

    for i in range(5):
        plt.text(x=0, y=15, s=i, fontdict=dict(fontsize=30, color='r'))
        plt.imshow(data_after_deal[i], cmap='gray')
        plt.savefig(f'..\\result\\after\\1\\{i}.png')
        plt.show()

    # 输出5张图片在一起的3d图像
    draw3d("..\\result\\after\\1\\", "..\\result\\after\\1\\", title="算法1降维后", n=5)
