package org.economygraph;

import java.io.File;
import java.io.IOException;

import org.apache.commons.cli.BasicParser;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.OptionBuilder;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.economygraph.util.Graph;
import org.economygraph.util.GraphNormalizer;
import org.economygraph.util.GraphReader;
import org.economygraph.util.GraphWriter;




public class Csv2graph {
	static boolean graphmlType = false;
	static String outputDirectory = "./output/";

	public static void main(String[] args) {
		String fileNameNodeMetadataFile, fileNameVectorFile;
		
		
		// CLI options
		Options options = new Options();
		// add g option
		options.addOption("g", false, "generate graphml, default dot format");

		// vectorfile
		@SuppressWarnings("static-access")
		Option vectorfile = OptionBuilder.withArgName( "file" )
                .hasArg()
                .isRequired()
                .withDescription("csv vector file" )
                .create( "vectorfile" );
		options.addOption(vectorfile);

		//nodefile
		@SuppressWarnings("static-access")
		Option nodefile = OptionBuilder.withArgName( "file" )
                .hasArg()
                .withDescription("csv node file" )
                .create( "nodefile" );
		options.addOption(nodefile);

		//nodefile
		@SuppressWarnings("static-access")
		Option outputdir = OptionBuilder.withArgName( "outputdir" )
                .hasArg()
                .withDescription("output directory" )
                .create( "outputdir" );
		options.addOption(outputdir);
		
		
		// test
		fileNameNodeMetadataFile ="test/nodes.csv";
		fileNameVectorFile = "test/vectors.csv";
	
		CommandLineParser parser = new BasicParser();
		try {
			CommandLine cmd = parser.parse( options, args);
			if(cmd.hasOption("g")) {
				graphmlType = true;
			}			
			// vectorfile
			if(cmd.hasOption("vectorfile")) {
			    fileNameVectorFile = cmd.getOptionValue("vectorfile");
			}

			// nodefile
			if(cmd.hasOption("nodefile")) {
				fileNameNodeMetadataFile = cmd.getOptionValue("nodefile");
			}
			
			// outputdir
			if(cmd.hasOption("outputdir")) {
				outputDirectory = cmd.getOptionValue("outputdir") + "/";
			}
			
		} catch (ParseException e) {
			// automatically generate the help statement
			HelpFormatter formatter = new HelpFormatter();
			formatter.printHelp( "cvs2graph", options );			
		}
		
		new Csv2graph().test(fileNameNodeMetadataFile, fileNameVectorFile);
	}
	
	public void test(String fileNameNodeMetadataFile, String fileNameVectorFile){
		if(fileNameNodeMetadataFile!=null){
			File nodeMetadataFile = new File(fileNameNodeMetadataFile);
		}
		File vectorFile = new File(fileNameVectorFile);

		
		// Read graph
		
		// TODO read node metadata
		long t1 = System.currentTimeMillis();
		Graph graph = null;
		try {
			graph = GraphReader.readGraph(vectorFile);
		} catch (IOException e) {
			e.printStackTrace();
		}
		long t2 = System.currentTimeMillis();
		
		// create output directories
		File theFile = new File(outputDirectory);
		theFile.mkdirs();
		
		// normalize graph		
		GraphNormalizer normalizer = new GraphNormalizer();
		Graph graphNormalized = normalizer.normalize(graph, outputDirectory);
		long t3 = System.currentTimeMillis();
		
		System.out.println("Graph created: " + (t2-t1) + " ms");
		System.out.println("Graph normlization: " + (t3-t2) + " ms");
		System.out.println("Original Nodes: " + graph.getNumNodes() + " ,edges: " + graph.getNumEdges());
		System.out.println("Normalized Nodes: " + graphNormalized.getNumNodes() + " ,edges: " + graphNormalized.getNumEdges());
		
		
		// TODO optional normalization		
		
		// Write graph
		t2 = System.currentTimeMillis();
		try {
			// filename 
			String filename = vectorFile.getName();
			filename = filename.substring(0, filename.lastIndexOf("."));
			
			
			// original
			File fOut;
			if(!graphmlType){
				fOut = new File(outputDirectory + filename + ".dot");
				GraphWriter.writeGraphDot(graph, fOut, null);
			} else {
				fOut = new File(outputDirectory + filename + ".graphml");
				GraphWriter.writeGraphML(graph, fOut, null);				
			}
			
			// normalized
			if(!graphmlType){
				fOut = new File(outputDirectory + filename + "_normalized.dot");
				GraphWriter.writeGraphDot(graphNormalized, fOut, normalizer.getNodeDictionary_new_old());			
			} else {
				fOut = new File(outputDirectory + filename + "_normalized.graphml");
				GraphWriter.writeGraphML(graphNormalized, fOut, normalizer.getNodeDictionary_new_old()); // TODO include old NIU metadata			
			}
			
		} catch (IOException e) {
			e.printStackTrace();
		}
		t3 = System.currentTimeMillis();
		System.out.println("Graph written: " + (t3-t2) + " ms");
	}
	
	public static void usage(){
		System.out.println("Csv2dot vectorFile [nodeMetadataFile]");
	}
}
