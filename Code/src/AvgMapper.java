import java.io.IOException;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

public class AvgMapper extends MapReduceBase implements
		Mapper<LongWritable, Text, Text, Text> {
	@Override
	public void map(LongWritable key, Text value,
			OutputCollector<Text, Text> output, Reporter reporter)
			throws IOException {
		String[] line = value.toString().split(",");
		int edu;
		String state;
		int house;
		String county;
		int size;

		if (line.length == 5) {
			try {
				edu = Integer.parseInt(line[0]);
			} catch (Exception e) {
				edu = 0;
			}
			try {
				state = line[1]; // State
			} catch (Exception e) {
				state = "JU";
			}
			try {
				house = Integer.parseInt(line[2]);
			} catch (Exception e) {
				house = 0;
			}
			try {
				county = line[3];
			} catch (Exception e) {
				county = "NA";
			}
			try {
				size = Integer.parseInt(line[4]);
			} catch (Exception e) {
				size = 0;
			}

			output.collect(new Text(state + ", " + county), new Text(edu + ","
					+ house + "," + size));
		}

	}
}
