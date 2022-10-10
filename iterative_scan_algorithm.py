import networkx as nx
import link_aggregate_algorithm as laa

convergence_threshold=0.0001

# This method implements the iterative scan algorithm as mentioned in the paper
def iterative_scan(cluster,graph):
	
	cluster_subgraph = graph.subgraph(cluster)
	
	community_density = laa.density_scoring_function(cluster_subgraph)
	is_density_improved = False
	
	while not is_density_improved:
		N_set = list(cluster_subgraph.nodes)
		
		for vertex in cluster_subgraph.nodes:
			adj_nodes = graph.neighbors(vertex)
			N_set = list(set(N_set).union(set(adj_nodes)))
		
		for vertex in N_set:

			prior_vertex_list = set(cluster_subgraph.nodes)
			if vertex in prior_vertex_list:
				prior_vertex_list.remove(vertex)
			else:
				prior_vertex_list.add(vertex)
			if not prior_vertex_list:
				new_community_density=0
			else:
				new_community = graph.subgraph(list(prior_vertex_list))
				new_community_density = laa.density_scoring_function(new_community)
			cur_community_density = laa.density_scoring_function(cluster_subgraph)
			if new_community_density > cur_community_density:
				cluster_subgraph = new_community.copy()
		modified_community_density = laa.density_scoring_function(cluster_subgraph)
		# If the new communication density does not increase based on a threshold, then it is converge.
		if abs(modified_community_density-community_density) < convergence_threshold:
			is_density_improved = True
		else:
			community_density = modified_community_density
	# return new communities
	return list(cluster_subgraph.nodes)