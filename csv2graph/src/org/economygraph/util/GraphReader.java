package org.economygraph.util;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

public class GraphReader {
	private GraphReader(){}
	
	public static Graph readGraph(String filename) throws IOException{		
		return readGraph(new File(filename));
	}
	
	public static Graph readGraph(File f) throws IOException{		
		BufferedReader br = null;
		br = new BufferedReader(new FileReader(f));
		String line;
		
		Graph g = new Graph();
		long cnt = 0;
		
		while((line = br.readLine()) != null){
			String[] parts=line.split(",");
			
			// ignore first line
			if((parts.length == 3) && (cnt > 0)){
				long idsource = Long.parseLong(parts[0]);
				long idtarget = Long.parseLong(parts[1]);
				Double weight = Double.parseDouble(parts[2]);

				Edge edge = new Edge(idsource, idtarget, weight);
				g.addEdge(edge);
			}
			cnt++;
		}

		if(br != null){
			br.close();			
		}	
		return g;
	}
}
