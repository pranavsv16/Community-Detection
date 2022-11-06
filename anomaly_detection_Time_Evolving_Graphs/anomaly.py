import random
import sys
import matplotlib.pyplot as plt
import time
from scipy.sparse import csr_matrix
from scipy.sparse import lil_matrix
from scipy.sparse import eye
from scipy.sparse.linalg import spsolve
import numpy as np
import math

# helper functions 

# function to get adjacency matrix representation from txt file
def find_adjacency_matrix(data_file):
    file_open = open(data_file, 'r')
    num_of_nodes,num_of_edges = next(file_open).split(" ")
    num_of_nodes = int(num_of_nodes)
    Adjanceny_mat = lil_matrix((num_of_nodes,num_of_nodes),dtype=float)
    for line in file_open.readlines():
        nodes = line.split(" ")
        node_1,node_2 = int(nodes[0]),int(nodes[1])
        
        Adjanceny_mat[node_1,node_2] = 1
        Adjanceny_mat[node_2,node_1] = 1
    file_open.close()
    return Adjanceny_mat, num_of_nodes

# function to get the degree matrix from the adjancency matrix
def find_degree_matrix(A,num_of_nodes):
    degree_mat = lil_matrix((num_of_nodes,num_of_nodes),dtype=float)
    for i in range(num_of_nodes):
        val = A[i].sum()
        degree_mat[i,i] = val
    return degree_mat

# functio to calculate the rooted formula from the paper
def rooted(S_1,S_2):
    inside_val = np.sqrt(S_1)-np.sqrt(S_2)
    return np.sqrt(np.sum(np.square(inside_val)))

# function to calculate the moving avergae of the similarities
def get_moving_avg(sim_array):
    
    ma = []
    for i in range(0,len(sim_array)-1):
        ma.append(abs(sim_array[i]-sim_array[i+1]))
    
    return np.sum(ma)/(len(sim_array)-1)

# function to save the txt file
def save_file(data_file, similarity_array):
    np.savetxt("output/"+data_file+'_time_series.txt',similarity_array)

# function to plot the time series data
def plot_time_series_data(data_file, similarity_array):
    
    time_series_median = np.median(similarity_array)
    moving_avg_mean = get_moving_avg(similarity_array)
    time_series_upper_threshold = time_series_median+3*moving_avg_mean
    time_series_lower_threshold = time_series_median-3*moving_avg_mean

    figure = plt.figure()
    plt.axhline(y=time_series_upper_threshold,linestyle='-',color='red')
    plt.axhline(y=time_series_lower_threshold,linestyle='-',color='red')
    plt.style.use('default')
    plt.plot(similarity_array,'.',color='black')
    figure.savefig("output/"+data_file+'_time_series.png')

if __name__=="__main__":
    start_time = time.time()
    print("Start of Anomaly Detection of Time Evolving Graphs")
    data_file = str(sys.argv[1])
    data_file_path = "datasets/datasets/"+data_file+"/"
    data_file_counts = {}
    data_file_counts["autonomous"] = 733
    data_file_counts["enron_by_day"] = 749
    data_file_counts["p2p-Gnutella"] = 9
    data_file_counts["voices"] = 38
    
    graph_count = data_file_counts[data_file]
    similarity_array = []

    for i in range(1, graph_count):
        
        graph1 = data_file_path+str(i-1)+"_"+data_file+".txt"
        graph2 = data_file_path+str(i)+"_"+data_file+".txt"

        # get corresponding information from graph 1
        graph1_A,nodes_1 = find_adjacency_matrix(graph1)
        graph1_D = find_degree_matrix(graph1_A,nodes_1)
        graph1_A = csr_matrix(graph1_A)
        graph1_D = csr_matrix(graph1_D)

        # get corresponding information from graph 2
        graph2_A,nodes_2 = find_adjacency_matrix(graph2)
        graph2_D = find_degree_matrix(graph2_A,nodes_2)
        graph2_A = csr_matrix(graph2_A)
        graph2_D = csr_matrix(graph2_D)

        epsilon = 0.9
        n_nodes = nodes_1
        identity_mat = eye(n_nodes)
        identity_mat = csr_matrix(identity_mat)
        
        nodes = list(range(0,n_nodes))
        group_count = max(int(n_nodes/100),20)
        
        random.shuffle(nodes)
        groups = [nodes[i::group_count] for i in range(group_count)]

        # calculate S for all gorups
        mat_s = np.zeros((n_nodes,group_count))
        for k in range(0,group_count):
            for i in groups[k]:
                mat_s[i][k] = 1
        mat_s = np.array(mat_s)
        
        S_1 = spsolve((identity_mat+(graph1_D*math.pow(epsilon,2))-(graph1_A*epsilon)),mat_s)
        S_2 = spsolve((identity_mat+(graph2_D*math.pow(epsilon,2))-(graph2_A*epsilon)),mat_s)
        
        # calculate rooted value
        d = rooted(S_1, S_2)

        # calculate similarity value
        similarity = 1/(1+d)
        similarity_array.append(similarity)

    save_file(data_file, similarity_array)
    plot_time_series_data(data_file, similarity_array)
    end_time = time.time()
    print("End of Anomaly Detection of Time Evolving Graphs")
    print("Time taken: ", round(end_time-start_time,3)," seconds")
   


