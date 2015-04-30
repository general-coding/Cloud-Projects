import java.awt.BorderLayout;
import java.io.*;
import java.text.SimpleDateFormat;
import java.util.*;

import weka.clusterers.*;
import weka.core.Instances;
import weka.gui.explorer.ClustererPanel;
import weka.gui.visualize.PlotData2D;
import weka.gui.visualize.VisualizePanel;

	public class wekatest {
	public static void main(String args[])throws Exception{
		//DataInputStream dis=new DataInputStream(System.in);

		//Instances instances=source.getDataSet();
		BufferedReader inputReader = new BufferedReader(new FileReader(args[0]));
		Integer clustNum = Integer.parseInt(args[1]); 
		Instances dataa = new Instances(inputReader);
		String outfile = "/var/www/html/wekaout.csv";
		BufferedWriter outputWriter = new BufferedWriter(new FileWriter(outfile));
		inputReader.close();
		// create the model 
		    SimpleKMeans kMeans = new SimpleKMeans();
		    kMeans.setNumClusters(clustNum);
		    kMeans.buildClusterer(dataa); 

		    // print out the cluster centroids
		    Instances centroids = kMeans.getClusterCentroids(); 
		    for (int i = 0; i < centroids.numInstances(); i++) { 
		      System.out.println( "Centroid " + i+1 + ": " + centroids.instance(i)); 
		    } 

		    // get cluster membership for each instance 
		    outputWriter.write("Year,HPCP,Cluster\n");
		    for (int i = 0; i < dataa.numInstances(); i++) { 
		      System.out.println( dataa.instance(i) + " is in cluster " + kMeans.clusterInstance(dataa.instance(i)) + 1); 
		      outputWriter.write(dataa.instance(i) + ","+kMeans.clusterInstance(dataa.instance(i))+"\n");
		    }
		    outputWriter.close();
		    //evaluate cluster
		    ClusterEvaluation eval=new ClusterEvaluation();
		    eval.setClusterer(kMeans);
		    eval.evaluateClusterer(dataa);
		  
		}
	}



