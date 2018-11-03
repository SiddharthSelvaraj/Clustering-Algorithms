# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 18:07:01 2018

@author: Siddharth
"""

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix
import matplotlib.cm as CM


# DBSCAN function
def DBSCAN(attributes, cluster, visited):
    Type=np.zeros(len(attributes))
    cluster_count=0
    for i in range(len(attributes)):
        if visited[i] == False:
            visited[i] = True
            neighbor_points = getNeighbors(i,len(attributes))
            # If neighbor points are greater or equal to the minimum points increase cluster count and add to cluster
            if len(neighbor_points) >= min_points:
                cluster_count+=1
                ExpandCluster(i, neighbor_points, cluster_count, cluster, visited)     
            # If neighbor points are lesser than minimum points classifiy it as noise
            else:
                Type[i]=-1


# Expand cluster function         
def ExpandCluster(P, neighbor_points, cluster_count, cluster, visited):
    cluster[P] = cluster_count
    k=0
    while k<len(neighbor_points):
        i=neighbor_points[k]
        if visited[i] == False:
            new_points = getNeighbors(i,len(data))
            visited[i] = True
            if len(new_points) >= min_points:
            # Merge new points to neighbor points
               neighbor_points.extend(new_points)
        if cluster[i] == 0:
            cluster[i] = cluster_count
        k+=1
               
# Function to get neighbors within eps radius.
def getNeighbors(P,genes):
    neighbor_points = list()
    for i in range(0, genes):
        if dist_matrix[P][i] <= eps:
            neighbor_points.append(i)
    return neighbor_points
   
# Function to visualize clustering results by PCA        
def plot_pca(attributes, cluster):
    pca_data = PCA(n_components=2).fit_transform(attributes)
    labels=list(set(cluster))
    # Color vector creation
    cvec=CM.brg(np.linspace(0,1,num=len(labels))) 
    legend_list=[]
    plt.figure(figsize=(10,7.5))
    for i in range(len(labels)):
        plot_data = pca_data[np.where(cluster==labels[i])]
        x=plot_data[:,0]
        y=plot_data[:,1]
        legend_list.append(plt.scatter(x, y, c=cvec[i],s=10))   
    labels=[-1.0 if x==0 else x for x in labels]
    labels=np.array(labels,dtype=int)
    plt.legend(legend_list,labels,loc="best")
    plt.xlabel("PC 1")
    plt.ylabel("PC 2")
    plt.title("DBSCAN: "+filename,fontweight="bold") 
    plt.show() 

# Inputting the file
filename=input("Enter the filename: ")
with open(filename) as textFile:
    lines=[line.split() for line in textFile]
data=np.asarray(lines)

# Input eps value
eps=float(input("Enter the eps: "))

# Input minimum points
min_points=int(input("Enter the minimum points: "))

# Obtaining attributes
attributes=np.matrix(data[:,2:],dtype=float,copy=False)

# Compute distance matrix from the attributes
dist_matrix=distance_matrix(attributes,attributes)

# Obtaining the ground truth
ground_truth=data[:,1]

# Initialize the clusters to zero
cluster=np.zeros(len(data))

# Initialize visited to false
visited=np.zeros(len(data),dtype=bool)

#DBSCAN function call  
DBSCAN(attributes, cluster, visited)

#compute jaccard coefficient and rand index
m_11=m_00=m_10=m_01=0
for i in range(len(data)):
    for j in range(len(data)): 
        if ground_truth[i]==ground_truth[j]:
            if cluster[i]==cluster[j]:
                m_11=m_11+1
            else:
                m_01=m_01+1
        elif ground_truth[i]!=ground_truth[j]:
            if cluster[i]==cluster[j]:
                m_10=m_10+1
            else:
                m_00=m_00+1  
jaccard=(m_11)/(m_11+m_10+m_01)
rand_index=(m_11+m_00)/(m_11+m_00+m_10+m_01)

#PCA_plot function call
plot_pca(attributes, cluster)

# Print the results
print("Jaccard Coefficient = ",jaccard)
print("Rand Index = ",rand_index)


