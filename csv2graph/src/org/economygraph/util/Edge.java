package org.economygraph.util;


public class Edge {
	private Number weight = 0.0;
	private long source;
	private long target;

	public Edge(long source, long target, Number weight){
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

	public long getSource() {
		return source;
	}

	public void setSource(long source) {
		this.source = source;
	}

	public long getTarget() {
		return target;
	}

	public void setTarget(long target) {
		this.target = target;
	}
}
