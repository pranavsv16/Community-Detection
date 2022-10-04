import networkx as nx

def density_scoring_function(sub_graph):
    return float(2 * nx.number_of_edges(sub_graph) / nx.number_of_nodes(sub_graph))

# order the vertex by pagerank
def page_rank_ordering(graph):
    vertices_dict = nx.pagerank(graph)
    sorted_vertices_tuple = tuple(sorted(vertices_dict.items(),key=lambda x:x[1], reverse=True))
    sorted_vertices_list = []
    sorted_vertices_list = list(zip(*sorted_vertices_tuple))[0]
    return sorted_vertices_list


def Link_Aggregate_Algorithm(G):
    output_clusters = []
    page_rank_vertices = page_rank_ordering(G)
    # Iterate through each vertex
    for vertex in page_rank_vertices:
        is_vertex_added = False
		# Iterate through all existing cluster to search if current vertex belongs to one of them
        for cluster in output_clusters:
            
            cluster_weight = density_scoring_function(G.subgraph(cluster))
            
            upated_cluster = cluster.copy()
            upated_cluster.append(vertex)
            
            updated_cluster_weight = density_scoring_function(G.subgraph(upated_cluster))
            
            if updated_cluster_weight > cluster_weight:
                cluster.append(vertex)
                is_vertex_added = True
		# If the vertex doesn't belong to one of the existing cluster, create a new cluster
        if not is_vertex_added:
            output_clusters.append([vertex])
	# Return a list of cluster 
    return output_clusters

