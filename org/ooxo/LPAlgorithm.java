package org.ooxo;

import java.io.*;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Scanner;
import java.util.Set;
import java.util.TreeSet;
import java.util.HashMap;
import org.json.JSONArray;
import org.json.JSONException;

abstract class LPAlgorithm {
	protected class Edge {
		Edge(long src_, long dest_, double weight_) {
			src    = src_;
			dest   = dest_;
			weight = weight_;
		}
		private long src;
		private long dest;
		private double weight;
		
		public long getSrc() {
			return src;
		}
		public long getDest() {
			return dest;
		}
		public double getWeight() {
			return weight;
		}
	}
	
	private class ReadJSON {
		ReadJSON(String fileName) {
			fFile = new File(fileName);
		}
		
		void processLineByLine() throws FileNotFoundException {
			Scanner scanner = new Scanner(new FileReader(fFile));
			try {
				while (scanner.hasNextLine()) {
					processLine(scanner.nextLine());
				}
			} finally {
				scanner.close();
			}
		}
		void processLine(String line) {
			try {
				// [vertexId, vertexLabel, edges]
				// unlabeled vertex if vertexLabel == 0
				// i.e. [2, 1, [[1, 1.0], [3, 1.0]]]
				JSONArray json = new JSONArray(line);
				Long vertexId = json.getLong(0);
				Long vertexLabel = json.getLong(1);
				JSONArray edges = json.getJSONArray(2);
				ArrayList<Edge> edgeArray = new ArrayList<Edge>();
				vertexLabelMap.put(vertexId, vertexLabel);
				for (int i = 0; i < edges.length(); ++i) {
					JSONArray edge = edges.getJSONArray(i);
					Long destVertexId = edge.getLong(0);
					Double edgeWeight = edge.getDouble(1);
					edgeArray.add(new Edge(vertexId, destVertexId, edgeWeight));
				}
				vertexAdjMap.put(vertexId, edgeArray);
			} catch (JSONException e) {
				throw new IllegalArgumentException(
						"Coundn't parse vertex from line: " + line, e);
			}
		}
		// private
		private File fFile;
	}
	
	LPAlgorithm() {
		vertexAdjMap   = new HashMap<Long, ArrayList<Edge>>();
		vertexInAdjMap = new HashMap<Long, ArrayList<Edge>>();
		vertexDegMap   = new HashMap<Long, Double>();
		vertexLabelMap = new HashMap<Long, Long>();
		labelIndexMap  = new HashMap<Long, Long>();
		vertexFMap     = new HashMap<Long, ArrayList<Double>>();
	}

	boolean loadJSON(String fileName) {
		ReadJSON reader = new ReadJSON(fileName);
		try {
			reader.processLineByLine();
		} catch (FileNotFoundException e) {
			System.err.println("Error: " + e.toString());
			return false;
		}
		// initialize vertexInAdjMap
		for (Long vertexId : vertexAdjMap.keySet()) {
			if (! vertexInAdjMap.containsKey(vertexId)) {
				vertexInAdjMap.put(vertexId, new ArrayList<Edge>());
			}
		}
		// setup vertexInAdjMap
		for (Long vertexId : vertexAdjMap.keySet()) {
			for (Edge e : vertexAdjMap.get(vertexId)) {
				vertexInAdjMap.get(e.getDest()).add(e);
			}
		}
		// setup vertexDegMap
		for (Long vertexId : vertexAdjMap.keySet()) {
			double degree = 0;
			if (vertexDegMap.containsKey(vertexId)) {
				degree = vertexDegMap.get(vertexId);
			}
			for (Edge e : vertexAdjMap.get(vertexId)) {
				degree += e.getWeight();
			}
			vertexDegMap.put(vertexId, degree);
		}
		// setup vertexFMap
		Set<Long> vSet = vertexLabelMap.keySet();
		Iterator<Long> it = vSet.iterator();
		Set<Long> lSet = new TreeSet<Long>();
		while (it.hasNext()) {
			
			Long l = vertexLabelMap.get(it.next());
			lSet.add(l);
			vertexSize++;
		}
		Iterator<Long> lSetIter = lSet.iterator();
		int labelEnum = 0;
		while (lSetIter.hasNext()) {
			Long l = lSetIter.next();
			if (l.intValue() == 0) continue;
			labelIndexMap.put(l, new Long(labelEnum));
			labelEnum++;
		}
		labelSize = labelEnum;
		it = vSet.iterator();
		labeledSize = 0;
		while (it.hasNext()) {
			Long v = it.next();
			ArrayList<Double> arr = new ArrayList<Double>(labelEnum);
			Long l = vertexLabelMap.get(v);
			if (l.intValue() == 0) {
				// unlabeled
				for (int i = 0; i < labelSize; ++i) {
					arr.add(0.0);
				}
			} else {
				// labeled
				labeledSize++;
				int ix = labelIndexMap.get(vertexLabelMap.get(v)).intValue();
				for (int i = 0; i < labelSize; ++i) {
					arr.add((i == ix) ? 1.0 : 0.0);
				}
			}
			vertexFMap.put(v, arr);
		}
		
		return true;
	}

	void showDetail() {
		System.out.println("Number of vertices:            " + vertexSize);
		System.out.println("Number of class labels:        " + labelSize);
		System.out.println("Number of unlabeled vertices:  " + (vertexSize - labeledSize));
		System.out.println("Numebr of labeled vertices:    " + labeledSize);
	}

	abstract void run(Double eps, Long maxIter);

	// private
	protected HashMap<Long,ArrayList<Edge>> vertexAdjMap; // out-edge
	protected HashMap<Long,ArrayList<Edge>> vertexInAdjMap;
	protected HashMap<Long, Double> vertexDegMap;
	protected HashMap<Long,Long> vertexLabelMap;
	protected HashMap<Long,Long> labelIndexMap; // todo: label as String, not Long
	protected HashMap<Long,ArrayList<Double>> vertexFMap;
	protected int vertexSize;
	protected int labelSize;
	protected int labeledSize;
}