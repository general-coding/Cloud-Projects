import java.io.IOException;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;

public class AvgTemperature {
	public static void main(String[] args) throws IOException {

		JobConf conf = new JobConf(AvgTemperature.class);
		conf.setJobName("Avg Temp");
		conf.setNumMapTasks(Integer.parseInt(args[2]));
		conf.setNumReduceTasks(Integer.parseInt(args[3]));

		double start_time = System.currentTimeMillis();
		conf.setOutputKeyClass(Text.class);
		conf.setOutputValueClass(Text.class);
		conf.setMapperClass(AvgMapper.class);
		conf.setReducerClass(AvgReducer.class);
		conf.setInputFormat(TextInputFormat.class);
		conf.setOutputFormat(TextOutputFormat.class);
		FileInputFormat.addInputPath(conf, new Path(args[0]));
		FileOutputFormat.setOutputPath(conf, new Path(args[1]));
		JobClient.runJob(conf);

		double end_time = System.currentTimeMillis();
		double elapsed_time = end_time - start_time;
		System.out.println("The total time taken to run is: " + elapsed_time);

	}
}
