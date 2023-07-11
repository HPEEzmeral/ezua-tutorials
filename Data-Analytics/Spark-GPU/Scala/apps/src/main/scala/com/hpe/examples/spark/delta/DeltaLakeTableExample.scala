package com.hpe.examples.spark.delta

import org.apache.spark.sql.SparkSession

object DeltaLakeTableExample {
  def main(args: Array[String]): Unit = {

    val sparkSession = SparkSession.builder
      .appName("Delta Lake Example")
      .getOrCreate()

    val df = sparkSession.createDataFrame(
      Seq(
        (1, "p1", "s1", 20),
        (1, "p2", "s1", 30),
        (1, "p1", "s2", 40),
        (1, "p2", "s2", 50),
        (2, "p1", "s1", 20),
        (2, "p2", "s1", 30),
        (2, "p1", "s2", 40),
        (2, "p2", "s2", 50)
      )
    )
      .toDF("day", "product", "store", "sales")

    df
      .write
      .format("delta")
      .save(args(0))

    sparkSession
      .read
      .format("delta").load(args(0))
      .show()

    println("DataFrame in DeltaLake is saved ")
    sparkSession.stop()
  }
}
