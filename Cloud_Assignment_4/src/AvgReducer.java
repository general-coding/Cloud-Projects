import java.io.IOException;
import java.util.Iterator;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;
import java.util.ArrayList;

public class AvgReducer extends MapReduceBase implements
		Reducer<Text, Text, Text, Text> {

	public static ArrayList<Integer> avgarray = new ArrayList<Integer>();
	public static ArrayList<Integer> avgprecparray = new ArrayList<Integer>();
	public static ArrayList<Integer> avgwindarray = new ArrayList<Integer>();

	@Override
	public void reduce(Text key, Iterator<Text> values,
			OutputCollector<Text, Text> output, Reporter reporter)
			throws IOException {
		String compTempRes = "";
		String compPrecp = "";
		String compWind = "";
		int sumTemp = 0;
		int sumprecp = 0;
		int sumwind = 0;
		int numItems = 0;
		while (values.hasNext()) {
			String nextValue = values.next().toString();
			String Cli[] = nextValue.split(",");
			int currenttemp = Integer.parseInt(Cli[0]);
			int currprecp = Integer.parseInt(Cli[1]);
			int currwind = Integer.parseInt(Cli[2]);
			sumTemp += currenttemp;
			sumprecp += currprecp;
			sumwind += currwind;
			numItems += 1;
		}
		int avgtemp = sumTemp / numItems;
		int avgprecp = sumprecp / numItems;
		int avgwind = sumwind / numItems;

		avgarray.add(avgtemp);
		avgprecparray.add(avgprecp);
		avgwindarray.add(avgwind);
		int sizetemp = avgarray.size();

		if (sizetemp > 1) {
			int compInt = avgarray.get(sizetemp - 2);
			if (compInt < avgtemp) {
				compTempRes = "Getting Warmer than Last Year";
			} else if (compInt > avgtemp) {
				compTempRes = "Getting Colder than Last Year";
			} else if (compInt == avgtemp) {
				compTempRes = "Same Result as Last Year";
			}
		}

		if (sizetemp > 1) {
			int compInt0 = avgprecparray.get(sizetemp - 2);
			if (compInt0 < avgprecp) {
				compPrecp = "Getting Wetter than Last Year";
			} else if (compInt0 > avgprecp) {
				compPrecp = "Getting Dryer than Last Year";
			} else if (compInt0 == avgprecp) {
				compPrecp = "Same Result as Last Year";
			}
		}

		if (sizetemp > 1) {
			int compInt1 = avgwindarray.get(sizetemp - 2);
			if (compInt1 > avgwind) {
				compWind = "Getting more windy than Last Year";
			} else if (compInt1 < avgwind) {
				compWind = "Getting less windy than Last Year";
			} else if (compInt1 == avgwind) {
				compWind = "Same Result as Last Year";
			}
		}

		String result = " ==== " + String.valueOf(avgtemp) + "DegF -"
				+ compTempRes + " ==== " + " ==== " + String.valueOf(avgprecp)
				+ "mm -" + compPrecp + " ==== " + String.valueOf(avgwind)
				+ "miles/hr - " + compWind;

		output.collect(key, new Text(result));

	}
}