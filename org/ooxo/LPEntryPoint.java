package org.ooxo;

import py4j.GatewayServer;
import org.apache.commons.cli.*;
// import java.lang.Double;
// import java.lang.Long;

public class LPEntryPoint {

    // private static String[] inputFileNames;
    // private static Double eps = new Double(10e-10);
    // private static Long maxIter = new Long(100);

    private LPAlgorithm lpa;

    public LPEntryPoint() {
        lpa = new LPAlgorithm();
    }

    public LPAlgorithm getLP() {
        return lpa;
    }

    public static void main(String[] args) {
        GatewayServer gatewayServer = new GatewayServer(new LPEntryPoint());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }

}