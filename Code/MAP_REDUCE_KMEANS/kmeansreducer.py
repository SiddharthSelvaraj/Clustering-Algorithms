#!/usr/bin/env python3
import sys
import numpy as np

d_data_matrix = []
centroids = []	


# splittng the line into individual data
for d_line in sys.stdin:
	if not d_line.strip():
		continue  # skip the empty line
	d_data = d_line.strip().split("\t")
	d_data_matrix.append(d_data)

 
    
#with open('.txt', 'w'):
#    for item in d_data_matrix:
#        f.write("%s\n" % d_line)

r_data_array = np.asarray(d_data_matrix, dtype = float)
r_cluster = r_data_array[:,0].astype(int)
r_attributes = np.delete(r_data_array,np.s_[0:1],axis = 1)

r_centroids = np.unique(r_cluster)
r_centroids_new = []
r_rows = r_attributes.shape[0]

#Updating centroids by taking mean of all points in a class
for i in range(len(r_centroids)):
    r_index_class = np.asarray([index for index, x in enumerate(r_cluster) if x == i])
    r_points_class = r_attributes[r_index_class,:]
        
    if len(r_points_class) == 0:
        r_centroids_new.insert(i, r_centroids[i])
            
    else:
        r_centroids_new.insert(i,np.mean(r_points_class, axis=0))

for j in range(len(r_centroids)):
    data_row = r_centroids_new[j]
    s = "\t"
    s = s.join(map(str, data_row))
    print(str(j)+"\t"+s)
    #data_final_file.write(str(j)+"\t"+s+"\n")
#data_final_file.close()