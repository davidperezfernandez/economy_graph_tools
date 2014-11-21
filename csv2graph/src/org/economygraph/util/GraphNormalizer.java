package org.economygraph.util;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

public class GraphNormalizer {
	static HashMap<Integer,Integer> nodeDictionary_new_old;
	static HashMap<Integer,Integer> nodeDictionary_old_new;
	
	public GraphNormalizer(){
		// Create node dictionaries
		nodeDictionary_new_old = new HashMap<Integer,Integer>(1000000);
		nodeDictionary_old_new = new HashMap<Integer,Integer>(1000000);		
	}

	
	public Graph normalize(Graph originalGraph, String outputDirectory) {		
		int numNodes = 0;

		Map<Integer, Edge> edges = originalGraph.getEdges();
		Iterator<Map.Entry<Integer, Edge>> iteratorEdges = edges.entrySet().iterator();
		
		while (iteratorEdges.hasNext()) {
			Map.Entry<Integer, Edge> entry =  iteratorEdges.next();    			
			Edge edge = entry.getValue();       
			
			int source = edge.getSource();
			int target = edge.getTarget();

        	if(!nodeDictionary_old_new.containsKey(target)){
        		nodeDictionary_new_old.put(numNodes, target);
        		nodeDictionary_old_new.put(target, numNodes++);
        	}
        	if(!nodeDictionary_old_new.containsKey(source)){
        		nodeDictionary_new_old.put(numNodes, source);
        		nodeDictionary_old_new.put(source, numNodes++);
        	}				
		}
		
		// store node dictionaries
		try {
			saveDictionary(nodeDictionary_new_old, nodeDictionary_old_new, outputDirectory);
		} catch (IOException e) {
			e.printStackTrace();
		}	
		
		Graph newGraph = traslateGraph(originalGraph, nodeDictionary_old_new);
		
		return newGraph;
	}
	
	
	private Graph traslateGraph(Graph originalGraph, HashMap<Integer, Integer> nodeDictionary_old_new) {
		Graph newGraph = new Graph(originalGraph.getNumEdges());

		Map<Integer, Edge> edges = originalGraph.getEdges();
		Iterator<Map.Entry<Integer, Edge>> iteratorEdges = edges.entrySet().iterator();
		
		while (iteratorEdges.hasNext()) {
			Map.Entry<Integer, Edge> entry =  iteratorEdges.next();    			
			Edge edge = entry.getValue();       
			
			int source = edge.getSource();
			int sourceNormalized = nodeDictionary_old_new.get(source);
						
			int target = edge.getTarget();
			int targetNormalized = nodeDictionary_old_new.get(target);
			
			Number weight = edge.getWeight();
			
			Edge newEdge = new Edge(sourceNormalized, targetNormalized, weight);
			newGraph.addEdge(newEdge);
		}		
		
		return newGraph;
	}


	private void saveDictionary(Map<Integer, Integer> DictionaryVertices_new_old, Map<Integer, Integer> DictionaryVertices_old_new, String outputDirectory) throws IOException{
		File fileDictionary_new_old = new File(outputDirectory + "dictionary_new_old.csv");
		File fileDictionary_old_new = new File(outputDirectory + "dictionary_old_new.csv");
		writeMap(DictionaryVertices_new_old, fileDictionary_new_old);
		writeMap(DictionaryVertices_old_new, fileDictionary_old_new);		
	}

	private void writeMap(Map<Integer, Integer> mapa, File file) throws IOException {
		PrintWriter pw=null;
		try {
			pw = new PrintWriter(new BufferedWriter(new FileWriter(file)));
			
			Iterator<Map.Entry<Integer, Integer>> it = mapa.entrySet().iterator();
			while (it.hasNext()) {
				Map.Entry<Integer, Integer> entry =  it.next();
				pw.println(entry.getKey() + "," + entry.getValue());
			}
		} catch (IOException e) {
			throw e;
			
		} finally{
			if(pw != null){
				pw.flush();
				pw.close();			
			}
		}		
	}


	public static HashMap<Integer, Integer> getNodeDictionary_new_old() {
		return nodeDictionary_new_old;
	}
	
}
