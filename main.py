import networkx as nx
import sys
import iterative_scan_algorithm as isa
import link_aggregate_algorithm as laa
import os

def fetch_word_from_path(input_file, word_num):
    words = input_file.split('/')
    return words[word_num]

def add_edges_to_graph(file, graph):
    for input_line in file:
        input_line = input_line.split()
        graph.add_edge(int(input_line[0]),int(input_line[1]))

def write_output_to_file(file, output):
    for fwd in output:
        line = " ".join(map(str, fwd))
        file.write(line + '\n')

def main():

    input_file_path = sys.argv[1]
    graph = nx.Graph()
    with open(input_file_path) as file:
        next(file)
        add_edges_to_graph(file, graph)
    print("Reading successful")
    clusters_using_laa = laa.Link_Aggregate_Algorithm(graph)
    final_output_clusters = []
    
    for cluster_laa in clusters_using_laa:
        final_output_clusters.append(isa.iterative_scan(cluster_laa, graph))
    
    final_output_without_duplicates = []
    for final_cluster in final_output_clusters:
        final_sorted_cluster = sorted(final_cluster)
        if final_sorted_cluster not in final_output_without_duplicates:
            final_output_without_duplicates.append(final_sorted_cluster)
    
    dir_path = "./output_results/"+fetch_word_from_path(input_file_path, 1)
    isDirExist = os.path.exists(dir_path)
    if not isDirExist:
        os.makedirs(dir_path)

    file_path = dir_path+"/"+fetch_word_from_path(input_file_path, 2)+".txt"
    with open(file_path, 'w') as file:
        write_output_to_file(file, final_output_without_duplicates)
    print("Output written successfully")
if __name__ == "__main__":
    main()