#!/usr/bin/env python3
import os
import sys
import numpy as np
from random import randint
from scipy.spatial import distance
from sklearn.decomposition import PCA


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


#Writing the centroids in a file
centroids_file = open("centroids.txt","w")
for i in centroids:
    s = "\t"
    s = s.join(str(j) for j in i) + '\n'
    centroids_file.write(s)
centroids_file.close()

#Getting the maximum  number of iterations from the user
no_of_iterations = int(input("Enter the max number of iterations: "))

os.system("$HADOOP_HOME/bin/hdfs dfs -rm -r "+"/user/hadoop/cent*")
os.system("$HADOOP_HOME/bin/hdfs dfs -rm "+file_name)
os.system("$HADOOP_HOME/bin/hdfs dfs -put "+file_name)
os.system("rm -r "+"kmeans_output*")

for i in range(no_of_iterations):

	os.system("hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.6.4.jar -file kmeansmapper.py -mapper kmeansmapper.py -file kmeansreducer.py -reducer kmeansreducer.py -file centroids.txt -input "+file_name+" -output centroids"+str(i))
	os.system("$HADOOP_HOME/bin/hdfs dfs -get centroids"+str(i)+" kmeans_output"+str(i))

	os.system("cp kmeans_output"+str(i)+"/part-00000 .")

	centroid_file_output = open("part-00000", "r")
	centroid_lines = centroid_file_output.readlines()
	centroid_matrix = []

	# splittng the line into individual data
	for l in centroid_lines:
    		centroid_data = l.strip().split("\t")
    		centroid_matrix.append(centroid_data)

	centroid_array = np.asarray(centroid_matrix, dtype = float)
	centroids_new = np.delete(centroid_array,np.s_[0:1],axis = 1)
	centroids_new_list = centroids_new.tolist();
	#Writing the centroids in a file
	centroids_file = open("centroids.txt","w")
	for i in centroids_new_list:
		s = "\t"
		s = s.join(str(j) for j in i) + '\n'
		centroids_file.write(s)
	centroids_file.close()
	#Checking if the centroids are same - if same break
	if np.array_equal(centroids, centroids_new):
		break
	centroids = centroids_new

#Assigning the data points to the respective centroids
cluster_assignment = []
for j in range(rows):
	centroid_dist = []
	for c in range(len(centroids)):
		centroid_dist.insert(c,distance.euclidean(attributes[j],centroids[c]))
	cluster_assignment.insert(j,centroid_dist.index(min(centroid_dist))+1)

#cluster_assignment=np.asarray(cluster_assignment)

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

#Writing the centroids in a file
cluster = open("cluster.txt","w")
for i in cluster_assignment:
	s = str(i) + '\t'
	cluster.write(s)
cluster.close()
