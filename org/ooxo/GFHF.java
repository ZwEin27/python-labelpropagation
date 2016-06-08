package org.ooxo;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.util.HashMap;
import java.util.ArrayList;

class GFHF extends LPAlgorithm {
	public GFHF(int _steps) {
		steps = _steps;
	}
	public GFHF() {
		steps = 10;
	}
	
	void debug() {
		ArrayList<Long> labels = new ArrayList<Long>(labelSize);
		for (Long label : labelIndexMap.keySet()) {
			labels.add(labelIndexMap.get(label).intValue(), label);
		}
		for (Long vertexId : vertexFMap.keySet()){
			ArrayList<Double> arr = vertexFMap.get(vertexId);
			System.out.printf("[%d,", vertexId);
			ByteArrayOutputStream buff = new ByteArrayOutputStream();
			PrintStream ps = new PrintStream(buff);
			double maxFVal = 0.0;
			int maxFValIx = 0;
			for (int i = 0; i < labelSize; ++i) {
				double fval = arr.get(i);
				if (fval > maxFVal) {
					maxFVal = fval;
					maxFValIx = i;
				}
				ps.printf("[%d,%.04f]", labels.get(i), arr.get(i));
				ps.printf(i != labelSize - 1 ? "," : "]\n");
			}
			System.out.print(labels.get(maxFValIx) + "," + buff.toString());
		}
	}
	
	double iter() {
		HashMap<Long,ArrayList<Double>> nextVertexFMap = new HashMap<Long,ArrayList<Double>>();
		// for all vertex
		double diff = 0.0;
		for (Long vertexId : vertexFMap.keySet()) {
			if (vertexLabelMap.get(vertexId) != 0) continue; // skip labeled
			// update F(vertexID) ... vetexFMap
			ArrayList<Double> nextFValue = new ArrayList<Double>();
			ArrayList<Double> fValues = vertexFMap.get(vertexId);
			for (int l = 0; l < labelSize; ++l) {
				// update f_l(vertexId)
				double fValue = 0.0;
				for (Edge e : vertexInAdjMap.get(vertexId)) {
					double w = e.getWeight();
					long src = e.getSrc();
					double deg = vertexDegMap.get(vertexId);
					fValue += vertexFMap.get(src).get(l) * (w / deg);
					//System.out.println("(src,dst): " + src + "->" + vertexId + ", value = (" + fValue +"), deg = " + deg + ", label = " + l);
				}
				nextFValue.add(fValue);
				if (vertexLabelMap.get(vertexId) == 0) {
					diff += ((fValue > fValues.get(l)) ? fValue - fValues.get(l) : fValues.get(l) - fValue);
				}
			}
			//System.out.println(nextFValue);
			nextVertexFMap.put(vertexId, nextFValue);
			//System.out.println("----");
		}
		// fix labeled vertex
		for (Long vertexId : vertexLabelMap.keySet()) {
			if (vertexLabelMap.get(vertexId) == 0) continue; // 0 means unlabeled vertex
			nextVertexFMap.put(vertexId, vertexFMap.get(vertexId));
		}
		vertexFMap = nextVertexFMap;
		
		return diff;
	}
	
	void run(Double eps, Long maxIter) {
		showDetail();
		System.out.println("eps:                           " + eps);
		System.out.println("max iteration                  " + maxIter);

		double diff = 0;
		int iter = 0;
		for (int i = 0; i < maxIter; ++i) {
			iter = i;
			System.out.print(".");
			System.out.flush();
			diff = iter();
			if (diff < eps) break;
			if (i % 50 == 49) {
				System.out.println("");
			}
		}
		System.out.println("\niter = " + (iter + 1) + ", eps = " + diff);
		debug();
	}
	
	// private
	final int steps;
}