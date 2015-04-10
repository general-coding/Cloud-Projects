// cc MaxTemperatureReducer Reducer for maximum temperature example
// vv MaxTemperatureReducer
import java.io.IOException;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class MaxTemperatureReducer extends
		Reducer<Text, IntWritable, Text, IntWritable> {

	@Override
	public void reduce(Text key, Iterable<IntWritable> values, Context context)
			throws IOException, InterruptedException {

		// int maxValue = Integer.MIN_VALUE;
		int sumvalue = 0;
		int total_records = 0;
		int average = Integer.MIN_VALUE;
		for (IntWritable value : values) {
			// maxValue = Math.max(maxValue, value.get());
			total_records = total_records + 1;
			sumvalue = sumvalue + value.get();
		}
		average = sumvalue / total_records;
		context.write(key, new IntWritable(average));
	}
}
// ^^ MaxTemperatureReducer
