package com.hpe.examples.spark.delta;

import org.apache.spark.api.java.function.MapFunction;
import org.apache.spark.sql.Encoders;
import org.apache.spark.sql.SparkSession;

public class DeltaLakeIntermediateFailExample {

    public static void main(String[] args) {

        //Job-1
        SparkSession spark = SparkSession.builder()
                .appName("Delta Lake Example")
                .getOrCreate();

        String filePath = args[0];

        spark
                .range(100, 200)
                .write()
                .format("delta")
                .mode("overwrite")
                .save(filePath);

        //Job-2
        try {
            spark.range(50, 150).map((MapFunction<Long, Integer>) num ->
                    {
                        if (num > 50) {
                            throw new RuntimeException("Atomicity failed");
                        }
                        return Math.toIntExact(num);
                    }, Encoders.INT()
            ).write().format("delta").mode("overwrite").option("overwriteSchema", "true").save(filePath);
        } catch (Exception e) {
            System.out.println("failed while OverWriteData");
        }

        //Job-3
        spark
                .range(50, 150)
                .write()
                .format("delta")
                .mode("overwrite")
                .save(filePath);

        spark
                .read()
                .format("delta")
                .load(args[0])
                .show(100);

        spark.stop();
    }
}
