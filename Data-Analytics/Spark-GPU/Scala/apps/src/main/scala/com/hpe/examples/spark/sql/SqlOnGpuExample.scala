package com.hpe.examples.spark.sql

import org.apache.spark.sql.SparkSession

object SqlOnGpuExample {

  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .getOrCreate()
    val sc = spark.sparkContext

    import spark.implicits._

    val viewName = "df"
    val df = sc.parallelize(Seq(1, 2, 3)).toDF("value")
    df.createOrReplaceTempView(viewName)

    spark.sql(s"SELECT value FROM $viewName WHERE value <>1").explain()
    spark.sql(s"SELECT value FROM $viewName WHERE value <>1").show()

    spark.stop()
  }

}
