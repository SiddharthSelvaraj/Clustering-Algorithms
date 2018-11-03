import numpy as np
from scipy.spatial import distance_matrix, distance
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.cm as CM
#np.set_printoptions(threshold=np.nan)

def findItem(list, item):
	return [(ind, list[ind].index(item)) for ind in range(len(list)) if item in list[ind]]

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
        legend_list.append(plt.scatter(x, y, c=cvec[i],s=10,alpha=0.9))   
    labels=[-1.0 if x==0 else x for x in labels]
    labels=np.array(labels,dtype=int)
    plt.legend(legend_list,labels,loc="best")
    plt.xlabel("PC 1")
    plt.ylabel("PC 2")
    plt.title("Hierarchical Agglomerative Clustering: "+file,fontweight="bold") 
    plt.show() 

file = input("Enter file name: ")
no_of_clusters = int(input("Enter the number of clusters: "))

file_path = open(file,'r')

data = np.loadtxt(file)

length = len(data[0])

gene_data = np.array(data[:,2:], dtype=float)
ground_truth = np.array(data[:,1], dtype=int)

#Reference : https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance_matrix.html
dist_mat = distance_matrix(gene_data,gene_data)

count = 0
label = [[x] for x in range(dist_mat.shape[0])]#list(range(dist_mat.shape[0]))
#label = label.astype(str)
while(count < gene_data.shape[0]-no_of_clusters):
	
	minimum = (dist_mat[dist_mat>0]).min()
	
	min_idx = np.where(minimum == dist_mat)[1]
	i=min_idx[1]
	j=min_idx[0]
	
	#print("i and j vals are ", i,j)
	for k in range(gene_data.shape[0]):
		dist_mat[i][k] = min(dist_mat[i][k],dist_mat[j][k])
		dist_mat[j][k] = np.inf
		dist_mat[k][i] = min(dist_mat[k][i],dist_mat[k][j])
		dist_mat[k][j] = np.inf
		dist_mat[k][k] = 0
	
	i_index = (findItem(label, i)[0])[0]
	j_index = (findItem(label, j)[0])[0]
	
	
	label[i_index] = label[i_index]+label[j_index]	
	label.pop(j_index)
	count = count + 1
print("LABEL VALUES ARE ",label)
#label = [x+1 for x in (label)]
for lab in label:
	for index,i in enumerate(lab):
		lab[index] += 1
for i in range(no_of_clusters):
	print(label[i])
label_list = [item for sublist in label for item in sublist]	



clusters = list(np.zeros(ground_truth.shape[0], dtype = int))
#clusters = [0] * ground_truth.shape[0]
clustername = 1
for lbls in list(label):
    for lbl in lbls:
        clusters[lbl-1] = clustername
    clustername += 1
	

#cluster_list = [item for sublist in clusters for item in sublist]	
clusters = np.asarray(clusters)

#compute jaccard coefficient and rand index
m_11=m_00=m_10=m_01=0
for i in range(len(data)):
    for j in range(len(data)): 
        if ground_truth[i]==ground_truth[j]:
            if clusters[i]==clusters[j]:
                m_11=m_11+1
            else:
                m_01=m_01+1
        elif ground_truth[i]!=ground_truth[j]:
            if clusters[i]==clusters[j]:
                m_10=m_10+1
            else:
                m_00=m_00+1  
jaccard=(m_11)/(m_11+m_10+m_01)
rand_index=(m_11+m_00)/(m_11+m_00+m_10+m_01)


plot_pca(gene_data,clusters)

print("Jaccard Coefficient = ",jaccard)
print("Rand Index = ",rand_index)
