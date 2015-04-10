// cc MaxTemperatureMapper Mapper for maximum temperature example
// vv MaxTemperatureMapper
import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class MaxTemperatureMapper extends
		Mapper<LongWritable, Text, Text, IntWritable> {

	private static final int MISSING = -9999;

	@Override
	public void map(LongWritable key, Text value, Context context)
			throws IOException, InterruptedException {

		String line = value.toString();
		String year_month = line.substring(51, 57);
		int airTemperature = MISSING;
		if (!line.substring(78, 83).equals("-9999")) { // parseInt doesn't like leading plus signs
			airTemperature = Integer.parseInt(line.substring(78, 83)
					.replaceAll("\\s+", ""));
		}
		if (airTemperature != MISSING) {
			context.write(new Text(year_month), new IntWritable(airTemperature));
		}
	}
}
