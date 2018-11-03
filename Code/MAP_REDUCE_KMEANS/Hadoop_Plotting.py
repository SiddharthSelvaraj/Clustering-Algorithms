import sys
import numpy as np
from random import randint
from scipy.spatial import distance
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.cm as CM

# Function to visualize clustering results by PCA
def plot_pca(attributes, cluster):
    pca_data = PCA(n_components=2).fit_transform(attributes)
    labels=list(set(cluster))
    # Color vector creation
    cvec=CM.Dark2(np.linspace(0,1,num=len(labels)))
    legend_list=[]
    for i in range(len(labels)):
        plot_data = pca_data[np.where(cluster==labels[i])]
        x=plot_data[:,0]
        y=plot_data[:,1]
        legend_list.append(plt.scatter(x, y, c=cvec[i],s=10))
    labels=np.array(labels,dtype=int)
    plt.legend(legend_list,labels,loc="best")
    plt.xlabel("PC 1")
    plt.ylabel("PC 2")
    plt.title("PCA: "+file_name,fontweight="bold")
    plt.show()

#Opening and reading the file line by line
file_name = input("Enter the name of the file: ")
file = open(file_name, "r")
lines = file.readlines()

data_matrix = []
data_matrix1 = list()
centroids = []

# splittng the line into individual data
for line in lines:
    data = line.strip().split("\t")
    data_matrix.append(data)

#Converting it into array and getting the gene id and ground truth
data_array = np.asarray(data_matrix, dtype = float)
gene_id = data_array[:,0]
ground_truth = data_array[:,1]
attributes = np.delete(data_array,np.s_[0:2],axis = 1)

file1 = open("cluster_assignment.txt", "r")
lines1 = file1.readlines()
for line in lines1:
    data1 = line.strip().split("\t")
    data_matrix1.extend(data1)

data_array1 = np.asarray(data_matrix1, dtype = float)
print(data_matrix1)
print(data_array1)
plot_pca(attributes, data_array1)
