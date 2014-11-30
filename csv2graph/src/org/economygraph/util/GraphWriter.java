package org.economygraph.util;


import java.io.BufferedOutputStream;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.text.NumberFormat;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Locale;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;




public class GraphWriter {
	private static final NumberFormat nf = NumberFormat.getInstance(Locale.ENGLISH);
	static {
		nf.setMaximumFractionDigits(20);
		nf.setMinimumFractionDigits(20);
	}
	 
	public static void writeGraphDot(Graph g, File f, HashMap<Long, Long> hashMap) throws IOException{		
		PrintWriter pw = new PrintWriter(new BufferedWriter(new FileWriter(f)));		
		Map<Integer,Edge> edges = g.getEdges();

		// header
		pw.print("digraph G {\n");
		
		// content

		// write nodes
		Set<Long> nodeSet = g.getNodes();
		for(Long node:nodeSet){
			// graph traslation
			if(hashMap != null){
				pw.print(node + " [NIU=" + hashMap.get(node) + "];\n");
			} else {
				pw.print(node + ";\n");
			}
		}
		
		// write edges
		Iterator<Map.Entry<Integer, Edge>> it = edges.entrySet().iterator();
		while (it.hasNext()) {
			Map.Entry<Integer, Edge> entry =  it.next();
			Edge edge = entry.getValue();
			pw.print(edge.getSource() + "->" + edge.getTarget() + " [w=\"" + edge.getWeight() + "\"];\n");			
		}
		
		// footer
		pw.print("}\n");
		
		
		if(pw != null){
			pw.flush();
			pw.close();			
		}		
	}

	public static void writeGraphML(Graph graph, File fOut, HashMap<Long, Long> nodeDictionary_new_old) throws IOException {
		FileOutputStream des=new FileOutputStream(fOut) ;
		BufferedOutputStream out= new BufferedOutputStream(des);
		boolean nodemetadata = false;
		
		int sizeG = graph.getEdges().size();
		Set<Long> listadoNodos = new HashSet<Long>(sizeG);
		
		// cabecera
		if(nodeDictionary_new_old != null){
			nodemetadata=true;	
		} 
		writeGraphMLHeader(out, nodemetadata);
		
		
		// nodos
		println(out, "\t<!-- vertices -->");
		
		Map<Integer, Edge> edges = graph.getEdges();
		Iterator<Entry<Integer, Edge>> iteratorEdges = edges.entrySet().iterator();
		
		
		while (iteratorEdges.hasNext()) {
			Entry<Integer, Edge> entry =  iteratorEdges.next();    			
			
			Edge ejeActual = entry.getValue();       
			
			long destino = ejeActual.getTarget();
			if(!listadoNodos.contains(destino)){
				listadoNodos.add(destino);
				if(nodemetadata){
					long niu = nodeDictionary_new_old.get(destino);
					println(out, "\t<node id=\"n" + destino + "\"><data key=\"niu\">" + niu +"</data></node>");
				} else {
					println(out, "\t<node id=\"n" + destino + "\"/>");
				}
			}
			
			long origen = ejeActual.getSource();
			if(!listadoNodos.contains(origen)){
				listadoNodos.add(origen);
				if(nodemetadata){
					long niu = nodeDictionary_new_old.get(origen);
					println(out, "\t<node id=\"n" + origen + "\"><data key=\"niu\">" + niu +"</data></node>");
				} else {
					println(out, "\t<node id=\"n" + origen + "\"/>");
				}
				
			}					
	    }		
	
		// edges
		println(out, "\n\t<!-- edges -->");		
		iteratorEdges = edges.entrySet().iterator();

		int cntEjes=0;
		while (iteratorEdges.hasNext()) {
			Map.Entry<Integer, Edge> entry =  iteratorEdges.next();    			
			Edge ejeActual = entry.getValue();    
			
	        long peso = ejeActual.getWeight().longValue();
	        if(peso!=0){
		       	println(out, "\t<edge id=\"e" + (cntEjes++) + "\" source=\"n" + ejeActual.getSource() 
						+ "\" target=\"n" + ejeActual.getTarget() +"\"><data key=\"w\">" + peso + "</data></edge>");			
	        }
	    }				
		
		// pie
		writeGraphMLFooter(out);
		
		// cierra
		out.flush();
		out.close();		
	}
	
	private static void writeGraphMLHeader(OutputStream out, boolean nodemetadata) throws IOException {
		println(out, "<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
		println(out, "<graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\"");
		println(out, "xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"");
		println(out, "xsi:schemaLocation=\"http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd\">");
		println(out, "");
		println(out, "\t<!-- property keys -->");
		println(out, "\t<key id=\"w\" for=\"edge\" attr.name=\"peso\" attr.type=\"float\" />");
		//TODO other node metadata
		// niu
		if(nodemetadata){
			println(out, "\t<key id=\"niu\" for=\"node\" attr.name=\"aeatNIU\" attr.type=\"int\" />");
		}
		println(out, "");
		println(out, "\t<graph id=\"G\" edgedefault=\"directed\" parse.nodeids=\"canonical\" parse.edgeids=\"canonical\" parse.order=\"nodesfirst\">");
		println(out, "");
		println(out, "\t<!-- graph properties -->");
		
	}
	
	private static void writeGraphMLFooter(OutputStream out) throws IOException {
		println(out, "\t</graph>");
		println(out, "</graphml>");
	}
	
	private static void println(OutputStream out, String line) throws IOException{		
		byte[] bytes=(line+"\n").getBytes();
		out.write(bytes);
	}	

}
