package org.ooxo;

import org.apache.commons.cli.*;
import java.lang.Double;
import java.lang.Long;

public class LProp
{
	private static String algoName;
	private static String[] inputFileNames;
	private static Double eps = new Double(10e-10);
	private static Long maxIter = new Long(100);

	private static void parseArgs(String[] args) {
		Options options = new Options();

		OptionBuilder.isRequired();
		OptionBuilder.hasArgs(1);
		options.addOption(OptionBuilder.create('a'));
		OptionBuilder.hasArgs(1);
		options.addOption(OptionBuilder.create('e'));
		OptionBuilder.hasArgs(1);
		options.addOption(OptionBuilder.create('m'));
		options.addOption(new Option( "help", "print this message" ));

		// TODO: add -s option: make given input symmetric
		CommandLineParser parser = new PosixParser();
		CommandLine cmd;

		try {
			cmd = parser.parse(options, args);
		} catch (ParseException exp) {
			System.err.println("Unexpected exception: " + exp.getMessage());
			return;
		}

		if (cmd.hasOption("help") || (!cmd.hasOption('a'))|| cmd.getArgs().length == 0) {
			HelpFormatter formatter = new HelpFormatter();
			formatter.printHelp("LProp FILE", options);
			System.exit(0);
		}
		if (cmd.hasOption('a') ){
			algoName = cmd.getOptionValue("a");
		}
		if (cmd.hasOption('e')) {
			eps = Double.parseDouble(cmd.getOptionValue("e"));
		}
		if (cmd.hasOption('m')) {
			maxIter = Long.parseLong(cmd.getOptionValue("m"));
		}

		inputFileNames = cmd.getArgs();
	}

	public static void main(String[] args) {
		parseArgs(args);

		LPAlgorithm lp = null;
		if (algoName.equals("GFHF")) {
			lp = new GFHF();
		} else {
			System.err.println("Specify algorithm with -a option.");
			System.exit(1);
		}
		lp.loadJSON(inputFileNames[0]);
		lp.run(eps, maxIter);
	}
}
