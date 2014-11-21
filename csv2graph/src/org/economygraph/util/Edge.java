package org.economygraph.util;


public class Edge {
	private Number weight = 0.0;
	private int source;
	private int target;

	public Edge(int source, int target, Number weight){
		this.source = source;
		this.target = target;
		this.weight = weight;
	}


	public Number getWeight() {
		return weight;
	}

	public void setWeight(Number weight) {
		this.weight = weight;
	}

	public int getSource() {
		return source;
	}

	public void setSource(int source) {
		this.source = source;
	}

	public int getTarget() {
		return target;
	}

	public void setTarget(int target) {
		this.target = target;
	}
}
