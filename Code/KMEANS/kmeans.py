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
    cvec=CM.rainbow(np.linspace(0,1,num=len(labels)))
    legend_list=[]
    for i in range(len(labels)):
        plot_data = pca_data[np.where(cluster==labels[i])]
        x=plot_data[:,0]
        y=plot_data[:,1]
        legend_list.append(plt.scatter(x, y, c=cvec[i],s=10))
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

#Using Forgy method to initalize the first centroids

k = int(input("Enter the k value: "))
print("k is set to be: "+str(k))

rows = attributes.shape[0]
cols = attributes.shape[1]

choice = input("Do you want to enter centroids 1.Yes 2.No (Enter 1 or 2)")

if choice == '1':
    for i in range(k):
        index = int(input("Enter the "+str(i+1)+" ID: "))
        centroids.append(attributes[index-1])
else:
    centroids = attributes[np.random.choice(rows, k, replace=False), :]


#Getting the maximum  number of iterations from the user
no_of_iterations = int(input("Enter the max number of iterations: "))

#https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.distance.euclidean.html
for i in range(no_of_iterations):
    #Assigning the data points to the respective centroids
    cluster_assignment = []
    for j in range(rows):
        centroid_dist = []
        for c in range(len(centroids)):
            centroid_dist.insert(c,distance.euclidean(attributes[j],centroids[c]))
        cluster_assignment.insert(j,centroid_dist.index(min(centroid_dist))+1)

    centroids_new = []
    #Updating centroids by taking mean of all points in a class
    for i in range(len(centroids)):
        index_class = np.asarray([index for index, x in enumerate(cluster_assignment) if x == i+1])
        points_class = attributes[index_class,:]

        if len(points_class) == 0:
            centroids_new.insert(i, centroids[i])

        else:
            centroids_new.insert(i,np.mean(points_class, axis=0))

    #Checking if the centroids are same - if same break
    if np.array_equal(centroids, centroids_new):
        break
    centroids = centroids_new

cluster_assignment=np.asarray(cluster_assignment)

#compute jaccard coefficient and rand index
m_00=m_11=m_10=m_01=0
for i in range(len(data_array)):
    for j in range(len(data_array)):
        if ground_truth[i]==ground_truth[j]:
            if cluster_assignment[i]==cluster_assignment[j]:
                m_11=m_11+1
            else:
                m_01=m_01+1
        elif ground_truth[i]!=ground_truth[j]:
            if cluster_assignment[i]==cluster_assignment[j]:
                m_10=m_10+1
            else:
                m_00=m_00+1
jaccard=(m_11)/(m_11+m_10+m_01)
rand_index=(m_11+m_00)/(m_11+m_00+m_10+m_01)

print("Jaccard Value: "+str(jaccard))
print("Rand Index Value: "+str(rand_index))

plot_pca(attributes, cluster_assignment)
