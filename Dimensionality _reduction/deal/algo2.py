import numpy as np
import random
import seaborn as sns
from PIL import Image
from matplotlib import pyplot as plt
from scipy.spatial.distance import euclidean
from scipy.stats import pearsonr
from skimage.io import imread
from skimage.metrics import structural_similarity as compare_ssim


# 假设图片被编号为0到199
from deal.draw_3d import draw3d


image_indices = list(range(200))
best_fitness_list = []


# 辅助函数，计算两张图片的MSSIM
def calculate_similarity(image1_idx, image2_idx):
    imageA = imread(f'../result/fore/{image1_idx}.png', as_gray=True)
    imageB = imread(f'../result/fore/{image2_idx}.png', as_gray=True)
    ssim, _ = compare_ssim(imageA, imageB, full=True)
    return ssim


# 适应度函数
def fitness_function(chromosome):
    similarity_sum = 0
    for i in range(len(chromosome)):
        for j in range(i + 1, len(chromosome)):
            similarity_sum += calculate_similarity(chromosome[i], chromosome[j])
    return 1 / similarity_sum  # 适应度是相似度之和的倒数


# 粒子群初始化
def initialize_particles(pop_size, gene_pool, chromosome_length):
    return [random.sample(gene_pool, chromosome_length) for _ in range(pop_size)]


# 更新粒子位置
def update_particles(particles, pbest_positions, gbest_position, velocity, gene_pool, w=0.5, c1=1, c2=2):
    new_particles = []
    new_velocity = []

    for i, particle in enumerate(particles):
        new_velocity_particle = []
        for j, value in enumerate(particle):
            r1 = random.random()
            r2 = random.random()
            vel_cognitive = c1 * r1 * (pbest_positions[i][j] - value)
            vel_social = c2 * r2 * (gbest_position[j] - value)
            new_vel = w * velocity[i][j] + vel_cognitive + vel_social
            new_velocity_particle.append(new_vel)

        new_particle = [gene_pool[int((value + new_velocity_particle[j]) % len(gene_pool))] for j, value in enumerate(particle)]
        new_particles.append(new_particle)
        new_velocity.append(new_velocity_particle)

    return new_particles, new_velocity


# 粒子群优化算法主函数
def particle_swarm_optimization(pop_size, gene_pool, chromosome_length, iterations, w=0.5, c1=1, c2=2):
    particles = initialize_particles(pop_size, gene_pool, chromosome_length)
    pbest_positions = particles.copy()
    pbest_fitness = [fitness_function(p) for p in particles]
    gbest_position = particles[np.argmax(pbest_fitness)]
    gbest_fitness = max(pbest_fitness)
    velocity = [[0 for _ in range(chromosome_length)] for _ in range(pop_size)]

    for i in range(iterations):
        for j, particle in enumerate(particles):
            current_fitness = fitness_function(particle)
            if current_fitness > pbest_fitness[j]:
                pbest_fitness[j] = current_fitness
                pbest_positions[j] = particle

        current_gbest_fitness = max(pbest_fitness)
        if current_gbest_fitness > gbest_fitness:
            gbest_fitness = current_gbest_fitness
            gbest_position = pbest_positions[np.argmax(pbest_fitness)]
        print(f'Generation {i} - Fitness_scores: {pbest_fitness}')
        print(f'Generation {i} - Best fitness: {max(pbest_fitness)}')
        best_fitness_list.append(gbest_fitness)
        particles, velocity = update_particles(particles, pbest_positions, gbest_position, velocity, gene_pool, w, c1, c2)

    # 绘制best_fitness_list的折线图
    plt.plot(best_fitness_list)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness(1/similarity)')
    plt.savefig('../result/after/2/best_fitness_train.png')
    plt.show()
    return gbest_position


# 运行粒子群优化算法
def run_algo2():
    best_solution = particle_swarm_optimization(
        pop_size=200,
        gene_pool=image_indices,
        chromosome_length=5,
        iterations=100,
        w=0.5,  # 惯性权重
        c1=1,   # 个体学习因子
        c2=2    # 社会学习因子
    )
    # result: [86, 0, 89, 74, 107] best fitness: 0.49928099557119093
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


def cal2():
    # 计算data_after_deal的5个维度图片相似性
    correlation_matrix = np.zeros((5, 5))
    data_after_deal = run_algo2()
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
    plt.title("PSO降维关联性矩阵")
    plt.xlabel("图片编号")
    plt.ylabel("图片编号")
    plt.savefig("..\\result\\after\\2\\algo2.png")
    plt.show()

    for i in range(5):
        plt.text(x=0, y=15, s=i, fontdict=dict(fontsize=30, color='r'))
        plt.imshow(data_after_deal[i], cmap='gray')
        plt.savefig(f'..\\result\\after\\2\\{i}.png')
        plt.show()

    # 输出5张图片在一起的3d图像
    draw3d("..\\result\\after\\2\\", "..\\result\\after\\2\\", title="算法2降维后", n=5)
