import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.cluster import KMeans

# 加载Iris数据集
iris = datasets.load_iris()
X = iris.data

# 应用K-means算法
kmeans = KMeans(n_clusters=3)
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

# 可视化聚类结果
plt.figure(figsize=(12, 8))
plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

centers = kmeans.cluster_centers_
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.6, edgecolor='black')
plt.title('K-means Clustering on Iris Dataset')
plt.xlabel('Sepal Length')
plt.ylabel('Sepal Width')
plt.show()
