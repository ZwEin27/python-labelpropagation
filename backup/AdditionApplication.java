package org.test.py4j;

import py4j.GatewayServer;

public class AdditionApplication {

  public int addition(int first, int second) {
    return first + second;
  }

  public static void main(String[] args) {
    AdditionApplication app = new AdditionApplication();
    // app is now the gateway.entry_point
    GatewayServer server = new GatewayServer(app);
    server.start();
  }
}


/*
sudo cp py4j0.10.1.jar /Library/Java/Extensions
 */