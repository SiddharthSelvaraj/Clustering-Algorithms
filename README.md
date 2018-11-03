# Clustering-Algorithms
---------KMEANS-----------
1. Place all the files in the same folder(input and code)
2. Run the code using "python3 kmeans.py" command
3. You will see the visualization and the external index


---------HEIRARCHICAL CLUSTERING-------------
To run Hierarchical Agglomerative clustering we need to run following commands:

>> python hac.py
Enter file name: iyer.txt
Enter the number of clusters: 10

>>python hac.py
Enter file name: cho.txt
Enter the number of clusters: 5

Output:
1. Data objects present in individual clusters
2. PCA based Plot of individual data objects with clusters values
3. Jaccard Coefficient and Rand index



-----------DBSCAN IMPLEMENTATION--------------
Place the datasets and the dbscan.py file in the same directory.
Run the python file dbscan.py
It prompts you to enter the filename with extension, the eps value and the minimum points.
After entering the required inputs, the output is displayed.
The jaccard coefficient and rand index values are printed
The PCA plot along with the clusters is displayed.



--------------MAP-REDUCE K MEANS---------------
1. Place all the files in the same folder(input and code) in the hadoop cluster
3. Start the hadoop using start-hadoop.sh"
2. Run the code using "python3 Main.py" command
3. You will get the output in cluster.txt
4. Now use the data in cluster.txt as input for the "Hadoop_Plotting.py" to plot the visualization
5. We must run "python3 Hadoop_Plotting.py" to get the final plots
