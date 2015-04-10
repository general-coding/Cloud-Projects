import java.io.IOException;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;
import org.apache.commons.lang.StringUtils;

public class AvgMapper extends MapReduceBase implements
		Mapper<LongWritable, Text, Text, Text> {
	@Override
	public void map(LongWritable key, Text value,
			OutputCollector<Text, Text> output, Reporter reporter)
			throws IOException {
		String[] line = value.toString().split(","); // splitting by ","
		String dataPart = line[2]; // Fetching Date
		String avgtemp = line[3]; // Fetching Temperature
		String precp = line[6]; // Fetching Precipitation
		String wind = line[13]; // Fetching Wind

		// String year = dataPart.substring(0,4);

		if (StringUtils.isNumeric(avgtemp)) {
			output.collect(new Text(dataPart), new Text(avgtemp + "," + precp
					+ "," + wind));
		}

	}
}
