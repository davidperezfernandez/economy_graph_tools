package org.economygraph.util;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;


public class Graph {
	private Map<Integer,Edge> edges;
	private int numEdges = 0;
	
	public Graph() {		
		edges = new HashMap<Integer,Edge>();
	}

	public Graph(int numEdges) {		
		edges = new HashMap<Integer,Edge>(numEdges);
	}
	
	public void addEdge(Edge edge) {
		edges.put(numEdges++, edge);		
	}

	public int getNumEdges() {
		return edges.size();
	}

	public long getNumNodes(){
		Set<Long> nodeSet = new HashSet<Long>();
		
		Iterator<Map.Entry<Integer, Edge>> iteratorEdges = edges.entrySet().iterator();    	
		while (iteratorEdges.hasNext()) {
			Map.Entry<Integer, Edge> entry =  iteratorEdges.next();    			
			
			Edge edge = entry.getValue();       
			
			long source = edge.getSource();
			long target = edge.getTarget();
			
			if(!nodeSet.contains(target)){
				nodeSet.add(target);
			}
			if(!nodeSet.contains(source)){
				nodeSet.add(source);
			}
	    }	
		return nodeSet.size();
	}

	public Set<Integer> getNodes(){
		Set<Integer> nodeSet = new HashSet<Integer>();
		
		Iterator<Map.Entry<Integer, Edge>> iteratorEdges = edges.entrySet().iterator();    	
		while (iteratorEdges.hasNext()) {
			Map.Entry<Integer, Edge> entry =  iteratorEdges.next();    			
			
			Edge edge = entry.getValue();       
			
			int source = edge.getSource();
			int target = edge.getTarget();
			
			if(!nodeSet.contains(target)){
				nodeSet.add(target);
			}
			if(!nodeSet.contains(source)){
				nodeSet.add(source);
			}
	    }	
		return nodeSet;
	}

	
	public Map<Integer,Edge> getEdges() {
		return edges;
	}
}



