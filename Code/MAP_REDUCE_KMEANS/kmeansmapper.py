#!/usr/bin/env python3
import sys
import numpy as np
from scipy.spatial import distance

c_file = open("centroids.txt", "r")
c_lines = c_file.readlines()

c_centroids = []
d_data_matrix = []

# splittng the line into individual centroids
for c_line in c_lines:
    c_data = c_line.strip().split("\t")
    c_centroids.append(c_data)


#Converting it into array
c_centroids_array = np.asarray(c_centroids, dtype = float)

#d_lines = open("cho.txt","r")
d_lines = sys.stdin.readlines()
# splittng the line into individual data
for d_line in d_lines:
    d_data = d_line.strip().split("\t")
    d_data_matrix.append(d_data)

#Converting it into array and getting the gene id and ground truth
d_data_array = np.asarray(d_data_matrix, dtype = float)
d_gene_id = d_data_array[:,0]
d_ground_truth = d_data_array[:,1]
d_attributes = np.delete(d_data_array,np.s_[0:2],axis = 1)


rows = d_attributes.shape[0]
cols = d_attributes.shape[1]
data_final_file = open("data_final.txt","w")
cluster_assignment = []
for j in range(rows):
    centroid_dist = []
    for c in range(len(c_centroids)):
        centroid_dist.insert(c,distance.euclidean(d_attributes[j],c_centroids_array[c]))
    cluster_assignment.insert(j,centroid_dist.index(min(centroid_dist)))
    data_row = d_attributes[j]
    s = "\t"
    s = s.join(map(str, data_row))
    print(str(cluster_assignment[j])+"\t"+s+"\n")
    data_final_file.write(str(cluster_assignment[j])+"\t"+s+"\n")
data_final_file.close()
