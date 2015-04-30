import weka.core.Instances;
import weka.core.converters.ArffSaver;
import weka.core.converters.CSVLoader;
import java.io.File;

public class weka {

	  public static void main(String[] args) throws Exception {
	    //if (args.length != 2) {
	    // System.out.println("\nUsage: CSV2Arff <input.csv> <output.arff>\n");
	     // System.exit(1);
	    //}
	 
	    // load CSV
	    CSVLoader loader = new CSVLoader();
	    //loader.setSource(new File("C:/Shree/Study/Cloud/Project 4 Hadoop/test.csv"));
	    System.out.println(args[0]);
	    System.out.println(args[1]);
	    loader.setSource(new File(args[0]));
	    Instances data = loader.getDataSet();
	 
	    // save ARFF
	    ArffSaver saver = new ArffSaver();
	    saver.setInstances(data);
	    //saver.setFile(new File("C:/Shree/Study/Cloud/Project 4 Hadoop/test.arff"));
	    saver.setFile(new File(args[1]));
	    //saver.setDestination(new File("C:/Shree/Study/Cloud/Project 4 Hadoop/test.arff"));
	    //saver.setDestination(new File(args[1]));
	    saver.writeBatch();
	  }
}


