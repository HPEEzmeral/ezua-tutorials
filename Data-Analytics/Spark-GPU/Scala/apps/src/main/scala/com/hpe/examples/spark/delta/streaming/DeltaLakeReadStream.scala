package com.hpe.examples.spark.delta.streaming

import org.apache.spark.sql.SparkSession

object DeltaLakeReadStream {

  def main(args: Array[String]): Unit = {

    val spark = SparkSession.builder
      .appName("Delta Lake Example")
      .getOrCreate()

    val df = spark.createDataFrame(Seq(
      (1, "p1", "s1", 20),
      (1, "p2", "s1", 30),
      (1, "p1", "s2", 40),
      (1, "p2", "s2", 50),
      (2, "p1", "s1", 20),
      (2, "p2", "s1", 30),
      (2, "p1", "s2", 40),
      (2, "p2", "s2", 50)))
      .toDF("day", "product", "store", "sales")

    df
      .write
      .format("delta")
      .save(args(0))

    println("DataFrame in DeltaLake is saved ")

    val streamingQuery = spark.readStream
      .format("delta")
      .load(args(0))
      .writeStream
      .format("console")
      .option("checkpointLocation", args(0) + "/_checkpoints/streaming-agg")
      .start()

    streamingQuery.awaitTermination();

    spark.stop()
  }
}
