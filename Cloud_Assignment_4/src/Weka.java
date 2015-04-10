import weka.core.Instances;
import weka.core.converters.ArffSaver;
import weka.core.converters.CSVLoader;
import java.io.File;

public class Weka {
	  public static void main(String[] args) throws Exception {	 
	    // load CSV
	    CSVLoader loader = new CSVLoader();
	    loader.setSource(new File("/home/puneeth/Desktop/CC/Quiz 4/big.csv"));
	    Instances data = loader.getDataSet();
	 
	    // save ARFF
	    ArffSaver saver = new ArffSaver();
	    saver.setInstances(data);
	    saver.setFile(new File("/home/puneeth/Desktop/CC/Quiz 4/output.arff"));
	    saver.setDestination(new File("/home/puneeth/Desktop/CC/Quiz 4/output.arff"));
	    saver.writeBatch();
	  }
}