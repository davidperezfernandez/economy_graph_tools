#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==========================================
#   Libraries and Packages
import networkx as nx
from src.stat_handler import StatsHandler
# ==========================================

class NetworkHandler:

	# -------------------------------------------------------------
    # 
    #  init (directory, name, weight_id, aggregate_number)
    # 
    # -------------------------------------------------------------

    def __init__(self, directory, name, weight_id, aggregate_number):

        self.name               = name
        self.directory          = directory 
        # self.G                  = nx.read_gexf(self.directory+self.name+'.gexf')
        self.G                  = nx.read_dot(self.directory+self.name+'.dot')
        self.weight_id          = weight_id
        self.features           = []
        self.aggregate_number   = aggregate_number
        self.Stats              = StatsHandler(name)
        
        self.standard_text_distribution = ',standard deviation,skewness,kurtosis,hhi,q90%,q80%,q70%,q60%,q50%,q40%,q30%,q20%,q10%,q5%,q1%'

    # -------------------------------------------------------------
    # 
    #  set_general_values()
    # 
    # -------------------------------------------------------------

    def set_general_values(self):

        general_values = []

        # size 
        general_values.append(len(self.G.nodes()))
        txt = ',number of nodes'
        # edges
        general_values.append(len(self.G.edges()))
        txt += ',number of edges'
        
        # nb lenders
        nb_lenders  = 0
        out_deg     = self.G.out_degree()
        for deg in out_deg.values():
            if deg > 0:
                nb_lenders += 1
        general_values.append(nb_lenders)
        txt += ',number of lenders'

        # nb borrowers
        nb_borrowers    = 0
        in_deg          = self.G.in_degree()
        for deg in in_deg.values():
            if deg > 0:
                nb_borrowers += 1
        general_values.append(nb_borrowers)
        txt += ',number of borrowers'

        return [general_values, txt]

    # -------------------------------------------------------------
    # 
    # set_degree_distribution
    #               computes cumulative distribution for 
    #                           all - in - out 
    #                                   and
    #               computes correlation between in and out
    # 
    # -------------------------------------------------------------

    def set_degree_analysis(self):

        degree_analysis = []
        txt             = ''
		
        # TOTAL
        self.degree_distribution    = self.G.degree()
        statistics                  = self.Stats.get_distribution_info(self.degree_distribution)
        #storing complete distribution for statistical analysis
        self.Stats.ks_store(self.degree_distribution, "total degree distribution")

        degree_analysis.extend(statistics[:5])
        degree_analysis.extend(statistics[5])
        txt += ',average degree' + self.standard_text_distribution
        
        # IN
        self.in_degree_distribution		= self.G.in_degree()
        statistics                      	= self.Stats.get_distribution_info(self.in_degree_distribution)
        #storing complete distribution for statistical analysis
        self.Stats.ks_store(self.in_degree_distribution, "in degree distribution")

        degree_analysis.extend(statistics[:5])
        degree_analysis.extend(statistics[5])
        txt += ',average in degree' + self.standard_text_distribution

        # OUT
        self.out_degree_distribution = self.G.out_degree()
        statistics = self.Stats.get_distribution_info(self.out_degree_distribution)
        #storing complete distribution for statistical analysis
        self.Stats.ks_store(self.out_degree_distribution, "out degree distribution")

        degree_analysis.extend(statistics[:5])
        degree_analysis.extend(statistics[5])
        txt += ',average out degree' + self.standard_text_distribution

        # CORRELATION
        keys  = self.G.nodes()
        d_in  = []
        d_out = []
        for key in keys:
            d_in.append(self.in_degree_distribution[key])
            d_out.append(self.out_degree_distribution[key])
        #storing complete distribution for statistical analysis
        self.Stats.r_square(d_in, d_out, "degree correlation" )
        
        degree_analysis.extend('A')
        txt += ',correlation in out degree'

        #ASSORTATIVITY
        d_1	= []
        d_2	= []
        for edge in self.G.edges():
            d_1.append(self.degree_distribution[edge[0]])
            d_2.append(self.degree_distribution[edge[1]])
        #storing complete distribution for statistical analysis
        self.Stats.r_square(d_1, d_2, "degree assortativity" )
        degree_analysis.extend('A')
        txt += ',assortativity'

        #RECIPROCITY
        density			= float(len(self.G.edges()))/(len(self.G.nodes())*(len(self.G.nodes())-1))
        reciprocal_value_num	= 0.0
        reciprocal_value_den	= 0.0
        for i in range(len(self.G.nodes())):
        	for j in range(len(self.G.nodes())):
        		if i != j:
        			a_ij = 0
        			a_ji = 0
        			if self.G.has_edge(self.G.nodes()[i],self.G.nodes()[j]):
        				a_ij = 1
        			if self.G.has_edge(self.G.nodes()[j],self.G.nodes()[i]):
        				a_ji = 1
        			reciprocal_value_num += (float(a_ij - density)*float(a_ji - density))
        			reciprocal_value_den += ((a_ij - density) * (a_ij - density))
        
        reciprocal_value = float(reciprocal_value_num)/reciprocal_value_den	
        degree_analysis.extend([reciprocal_value])
        txt += ',reciprocity'
        return [degree_analysis, txt]

    # -------------------------------------------------------------
    # 
    # set_volume_distribution()
    # 
    # -------------------------------------------------------------

    def set_volume_distribution(self):

        volume_analysis = []
        txt             = ''

        # TOTAL
        self.volume_distribution  = dict()
        for node in self.G.nodes():
                volume = 0.0
                for edge in self.G.edges(data = True):
                        if node in edge[1] or node in edge[0]:
                                volume += edge [2][self.weight_id]
                self.volume_distribution[node] = volume
        total_volume = sum(self.volume_distribution.values())
        volume_analysis.append(total_volume)
        
        statistics = self.Stats.get_distribution_info(self.volume_distribution)
        #storing complete distribution for statistical analysis
        self.Stats.ks_store(self.volume_distribution, "total volume distribution")

        volume_analysis.extend(statistics[:5])
        volume_analysis.extend(statistics[5])
        txt += ',full volume, average volume' + self.standard_text_distribution

        # IN
        self.in_volume_distribution  = dict()
        for node in self.G.nodes():
                volume = 0.0
                for edge in self.G.edges(data = True):
                        if node in edge[1]:
                                volume += edge [2][self.weight_id]
                self.in_volume_distribution[node] = volume
        tota_volume_in = sum(self.in_volume_distribution.values())
        volume_analysis.append(tota_volume_in)

        statistics = self.Stats.get_distribution_info(self.in_volume_distribution)
        #storing complete distribution for statistical analysis
        self.Stats.ks_store(self.in_volume_distribution, "total in volume distribution")

        volume_analysis.extend(statistics[:5])
        volume_analysis.extend(statistics[5])
        txt += ',full in volume, average in volume' + self.standard_text_distribution

        # OUT

        self.out_volume_distribution  = dict()
        for node in self.G.nodes():
                volume = 0.0
                for edge in self.G.edges(data = True):
                        if node in edge[0]:
                                volume += edge [2][self.weight_id]
                self.out_volume_distribution[node] = volume
        tota_volume_out = sum(self.out_volume_distribution.values())
        volume_analysis.append(tota_volume_out)

        statistics = self.Stats.get_distribution_info(self.out_volume_distribution)
        #storing complete distribution for statistical analysis
        self.Stats.ks_store(self.out_volume_distribution, "total out volume distribution")

        volume_analysis.extend(statistics[:5])
        volume_analysis.extend(statistics[5])
        txt += ',full out volume, average out volume' + self.standard_text_distribution

        # # correlation
        keys    = self.G.nodes()
        v_in    = []
        v_out   = []
        for key in keys:
            v_in.append(self.in_volume_distribution[key])
            v_out.append(self.out_volume_distribution[key])
        #storing complete distribution for statistical analysis
        self.Stats.r_square(v_in, v_out, "volume correlation" )

        volume_analysis.extend('A')
        txt += ',correlatin in out volume'
        
        return [volume_analysis, txt]

    # -------------------------------------------------------------
    # 
    # set_clustering_distribution ()
    # 
    # -------------------------------------------------------------

    def set_clustering_distribution(self):

        # only indirected
        G_undirected                = self.G.to_undirected()
        clustering_distributions    = []
        txt                         = ''

        # unweighted
        self.unweighted_clustering_distribution	= nx.clustering(G_undirected)
        statistics		= self.Stats.get_distribution_info(self.unweighted_clustering_distribution)
        #storing complete distribution for statistical analysis
        self.Stats.ks_store(self.unweighted_clustering_distribution, "unweighted clustering distribution")

        clustering_distributions.extend(statistics[:5])
        clustering_distributions.extend(statistics[5])
        txt += ',average clustering coeficient (unweighted)' + self.standard_text_distribution

        # # weighted
        self.weighted_clustering_distribution   = nx.clustering(G_undirected, G_undirected.nodes(), self.weight_id)
        # statistics	= self.Stats.get_distribution_info(self.weighted_clustering_distribution)
        # #storing complete distribution for statistical analysis
        # self.Stats.ks_store(self.weighted_clustering_distribution, "weighted clustering distribution")

        # clustering_distributions.extend(statistics[:5])
        # clustering_distributions.extend(statistics[5])
        # txt += ',average clustering coeficient (weighted)' + self.standard_text_distribution

        return [clustering_distributions,txt]

    # -------------------------------------------------------------
    # 
    # centrality_measures()
    # 
    # -------------------------------------------------------------

    def centrality_measures(self):

        centrality_measures = []
        txt = ''
        
        # betweenness
        # unweighted
        self.unweighted_betweenness_distribution	= nx.betweenness_centrality(self.G)
        statistics		= self.Stats.get_distribution_info(self.unweighted_betweenness_distribution)
        centrality_measures.extend(statistics[:5])
        centrality_measures.extend(statistics[5])
        txt += ',average betweenness centrality (unweighted)' + self.standard_text_distribution

        # # weighted
        self.weighted_betweenness_distribution		= nx.betweenness_centrality(self.G, weight = self.weight_id)
        # statistics		= self.Stats.get_distribution_info(self.weighted_betweenness_distribution)
        # centrality_measures.extend(statistics[:5])
        # centrality_measures.extend(statistics[5])
        # txt += ',average betweenness centrality (weighted)' + self.standard_text_distribution
        
        # closeness
        # unweighted
        self.unweighted_closeness_distribution	= nx.closeness_centrality(self.G)
        statistics		= self.Stats.get_distribution_info(self.unweighted_closeness_distribution)
        centrality_measures.extend(statistics[:5])
        centrality_measures.extend(statistics[5])
        txt += ',average closeness centrality (unweighted)' + self.standard_text_distribution        
        
        # eigen vector
		# right
        try:
            self.right_eigenvector_distribution	= nx.eigenvector_centrality(self.G)
            statistics	= self.Stats.get_distribution_info(self.right_eigenvector_distribution)
            centrality_measures.extend(statistics[:5])
            centrality_measures.extend(statistics[5])
        except:
            centrality_measures.extend([0,0,0,0,0])
            centrality_measures.extend([0]*len(statistics[5])) 
        txt += ',average right eigenvector' + self.standard_text_distribution
		
		# left
        try:
            G_rev 								= self.G.reverse()
            self.lef_eigenvector_distribution	= nx.eigenvector_centrality(G_rev)
            statistics							= self.Stats.get_distribution_info(self.lef_eigenvector_distribution)
            centrality_measures.extend(statistics[:5])
            centrality_measures.extend(statistics[5])
        except:
            centrality_measures.extend([0,0,0,0,0])
            centrality_measures.extend([0]*len(statistics[5])) 
        txt += ',average left eigenvector' + self.standard_text_distribution

        return [centrality_measures, txt]

    # -------------------------------------------------------------
    # 
    # transversal_measures()
    # 
    # -------------------------------------------------------------

    def transversal_measures(self):

        transversal_measures    = []
        txt = ''

        # - V(k) 
        # all
        title = "Vol(k) all"

        degrees  = []
        volumes  = []
        keys     = self.degree_distribution.keys()
        for key in keys:
            degrees.append(self.degree_distribution[key])
            volumes.append(self.volume_distribution[key])
        
        self.Stats.r_square(degrees, volumes, title )

        transversal_measures.extend('A')

        #  - in
        title = "Vol(k) in"

        in_degrees 	= []
        in_volumes 	= []
        keys 		= []
        keys            = self.in_degree_distribution.keys()
        for key in keys:
            in_degrees.append(self.in_degree_distribution[key])
            in_volumes.append(self.in_volume_distribution[key])
        self.Stats.r_square(in_degrees, in_volumes, title)

        transversal_measures.extend('A')

        title = "Vol(k) out"

        out_degrees = []
        out_volumes = []
        keys        = []
        keys        = self.out_degree_distribution.keys()
        for key in keys:
            out_degrees.append(self.out_degree_distribution[key])
            out_volumes.append(self.out_volume_distribution[key])
        self.Stats.r_square(out_degrees, out_volumes, title)

        transversal_measures.extend('A')

        # - C(k)
        G_undirected                    = self.G.to_undirected()
        undirected_degree_distribution  = G_undirected.degree()

        # unweighted cluster
        title = "C(k) unweighted"

        degrees                 = []       
        unweighted_clusters     = []
        keys                    = undirected_degree_distribution.keys()
        for key in keys:
            degrees.append(undirected_degree_distribution[key])
            unweighted_clusters.append(self.unweighted_clustering_distribution[key])
        self.Stats.r_square(degrees, unweighted_clusters, title)        

        transversal_measures.extend('A')

        # weighted cluster
        title = "C(k) weighted"

        degrees             = []
        weighted_clusters   = []
        keys = self.degree_distribution.keys()
        for key in keys:
            degrees.append(undirected_degree_distribution[key])
            weighted_clusters.append(self.weighted_clustering_distribution[key])
        self.Stats.r_square(degrees, weighted_clusters, title)   

        transversal_measures.extend('A') 

        # - Vij
        title = "Vij(kikj) with no aggregation"
        edges_volumes 	= []
        degrees 	= []
        for edge in self.G.edges(data = True):
            node1_degree            = self.out_degree_distribution[edge[0]]
            node2_degree            = self.in_degree_distribution[edge[1]]
            weight                  = edge[2][self.weight_id]
            edges_volumes.append(weight)
            degrees.append(node1_degree*node2_degree)
 
        self.Stats.r_square(degrees, edges_volumes, title)   

        transversal_measures.extend('A') 
        
        txt += ',correlation total volume degree,correlation in volume degree,correlation out volume degree,correlation unweighted cluster degree,correlation weighted cluster degree,correlation weight end degree product'
        
        return [transversal_measures,txt]

    # -------------------------------------------------------------
    # 
    # scc_analysis()
    # 
    # -------------------------------------------------------------

    def scc_analysis(self):
        
        scc_stats   = []
        txt         = ''
        
        #WGCC analysis
        wccs 	= nx.weakly_connected_component_subgraphs(self.G)
        n_wcc 	= len(wccs)
        # new to add to list!
        scc_stats.append(n_wcc)
        txt += ',number of wccs'

        nodes_in_lwcc   = nx.weakly_connected_components(self.G)[0]
        size		= len(self.G.nodes())
           
        # share in gwcc 
        share				= float(len(nodes_in_lwcc))/size
        lwcc                        	= wccs[0]
        avg_shortest_path_lentgh    	= nx.average_shortest_path_length(lwcc)

        scc_stats.extend([share,avg_shortest_path_lentgh])
        txt += ',LWCC - share of WCC,LWCC - shortest path length'        
        
        # number of nodes
        n = len(nodes_in_lwcc)
        # number of links
        l = len(lwcc.edges())
        # volume
        volume = 0.0
        for edge in lwcc.edges(data = True):
            volume += edge[2][self.weight_id]
        # new to add to list!
        scc_stats.extend([n,l,volume])
        txt += ',number of nodes,number of links,total volume'
    
        #LSCC analysis
        sccs = nx.strongly_connected_component_subgraphs(self.G)
        # number of sccs
        n_scc = len(sccs)
        scc_stats.append(n_scc)
        txt += ',number of sccs'
    
        # Bow Tie analysis for the largest SCC
        nodes_in_lscc   = nx.strongly_connected_components(self.G)[0]
        other_nodes     = list(set(self.G.nodes())^set(nodes_in_lscc))
        in_nodes        = []
        out_nodes       = []
            
        for node in other_nodes:
            edges   = self.G.edges()
            stop    = False
            i=0
            while (stop == False and i < len(edges)-1):
                if node in edges[i]:
                    if edges[i][1] in nodes_in_lscc:
                        in_nodes.append(node)
                        stop = True
                    else:
                        if edges[i][0] in nodes_in_lscc:
                            out_nodes.append(node)
                            stop = True
                i += 1

        disconnected_nodes  = list(set(other_nodes)^set(in_nodes)^set(out_nodes))
        size                = len(self.G.nodes())
        # scc_stats.extend([float(len(nodes_in_lscc))/size, float(len(in_nodes))/size, float(len(out_nodes))/size, float(len(disconnected_nodes))/size])
        
        # SCC
        # share in scc 
        share = float(len(nodes_in_lscc))/size
        lscc                        = sccs[0]
        avg_shortest_path_lentgh    = nx.average_shortest_path_length(lscc)
        diameter                    = nx.diameter(lscc)
        scc_stats.extend([share,avg_shortest_path_lentgh,diameter])
        txt += ',LSCC - share of scc,LSCC - shortest path lentgh,LSCC - diameter'
        
        # number of nodes
        n = len(nodes_in_lscc)
        # number of links
        l = len(lscc.edges())
        # volume of edges inside the lscc
        volume_edges = 0.0
        for edge in lscc.edges(data = True):
            volume_edges += edge[2][self.weight_id]
        # total, in and out volume of nodes inside the lscc
        total_volume_nodes = 0.0
        in_volume_nodes = 0.0
        out_volume_nodes = 0.0
        for node in lscc.nodes():
            total_volume_nodes += self.volume_distribution[node]
            in_volume_nodes += self.in_volume_distribution[node]
            out_volume_nodes += self.out_volume_distribution[node]

        scc_stats.extend([n,l,volume_edges,total_volume_nodes,in_volume_nodes,out_volume_nodes])
        txt += ',number of nodes, number of links,volume edges, total volume nodes, in volume nodes, out volume nodes'

        # IN
        # share
        share = float(len(in_nodes))/size
        # number of nodes
        n = len(in_nodes)
        # number of links
        # volume
        n_links = 0
        volume = 0.0
        for edge in self.G.edges(data=True):
#            if edge[0] in in_nodes or edge[1] in in_nodes:
            if edge[0] in in_nodes and edge[1] in lscc:
                n_links += 1
                volume += edge[2][self.weight_id]
        # total, in and out volume of nodes inside the IN
        total_volume_nodes = 0.0
        in_volume_nodes = 0.0
        out_volume_nodes = 0.0
        for node in in_nodes:
            total_volume_nodes += self.volume_distribution[node]
            in_volume_nodes += self.in_volume_distribution[node]
            out_volume_nodes += self.out_volume_distribution[node]
            
        scc_stats.extend([share,n,l,volume_edges,total_volume_nodes,in_volume_nodes,out_volume_nodes])
        txt += ',LSCC - share IN,number of nodes,number of links,volume edges,total volume nodes, in volume nodes, out volume nodes'
    
    
        # OUT
        # share
        share = float(len(out_nodes))/size
        # number of nodes
        n = len(out_nodes)
        # number of links
        # volume
        n_links = 0
        volume = 0.0
        for edge in self.G.edges(data=True):
#            if edge[0] in out_nodes or edge[1] in out_nodes:
            if edge[0] in lscc and edge[1] in out_nodes:
                n_links += 1
                volume += edge[2][self.weight_id]

        # total, in and out volume of nodes inside the IN
        total_volume_nodes = 0.0
        in_volume_nodes = 0.0
        out_volume_nodes = 0.0
        for node in out_nodes:
            total_volume_nodes += self.volume_distribution[node]
            in_volume_nodes += self.in_volume_distribution[node]
            out_volume_nodes += self.out_volume_distribution[node]
        scc_stats.extend([share,n,l,volume_edges,total_volume_nodes,in_volume_nodes,out_volume_nodes])
        txt += ',LSCC - share OUT,number of nodes,number of links,volume edges,total volume nodes, in volume nodes, out volume nodes'


        # EIGENVECTOR IN LSCC
		#right
        try:
            self.right_eigenvector_distribution_lscc = nx.eigenvector_centrality(lscc)
            statistics	= self.Stats.get_distribution_info(self.right_eigenvector_distribution_lscc)
            scc_stats.extend(statistics[:5])
            scc_stats.extend(statistics[5])
        except:
            scc_stats.extend([0,0,0,0,0])
            # MAKE THE NUMBER OF PERCENTILES VARIABLE!
            scc_stats.extend([0]*11) 
        txt += ',average right eigenvector lscc' + self.standard_text_distribution
		
		# left
        try:
            lscc_rev = lscc.reverse()
            self.lef_eigenvector_distribution_lscc	= nx.eigenvector_centrality(lscc_rev)
            statistics	= self.Stats.get_distribution_info(self.lef_eigenvector_distribution_lscc)
            scc_stats.extend(statistics[:5])
            scc_stats.extend(statistics[5])
        except:
            scc_stats.extend([0,0,0,0,0])
            scc_stats.extend([0]*11) 
        txt += ',average left eigenvector lscc' + self.standard_text_distribution
        
        
        # KATZ IN LSCC
        try:
            self.katz_distribution_lscc = nx.eigenvector_centrality(lscc)
            statistics	= self.Stats.get_distribution_info(self.katz_distribution_lscc)
            scc_stats.extend(statistics[:5])
            scc_stats.extend(statistics[5])
        except:
            scc_stats.extend([0,0,0,0,0])
            # MAKE THE NUMBER OF PERCENTILES VARIABLE!
            scc_stats.extend([0]*11) 
        txt += ',average katz centrality' + self.standard_text_distribution       
        return [scc_stats, txt]

# Giving work to Matlab
    def save_extra(self):
        self.Stats.save_ks_s()


