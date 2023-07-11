package com.hpe.examples.spark.delta

import org.apache.spark.sql.SparkSession
import io.delta.tables._

object DeltaLakeACIDExample {
  def main(args: Array[String]): Unit = {

    val sparkSession = SparkSession.builder
      .appName("Delta Lake ACID Example")
      .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
      .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
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

    println("DataFrame in DeltaLake is saved ")
    sparkSession
      .read
      .format("delta").load(args(0))
      .show()

    val dt = DeltaTable.forPath(args(0))

    println("Update record with sales increase by 5 for product p1 at store s1")
    dt.updateExpr("product == 'p1' AND store == 's1'", Map("sales" -> "sales + 5"))
    dt
      .toDF
      .show()

    println("Delete records for product p1")
    dt.delete("product == 'p1'")
    dt
      .toDF
      .show()

    println("Merge new records")
    val df1 = sparkSession.createDataFrame(
      Seq(
        (3, "p1", "s1", 219),
        (3, "p2", "s1", 321),
        (3, "p1", "s2", 303),
        (3, "p2", "s2", 419)
      )
    )
      .toDF("day", "product", "store", "sales")
    df1.show()

    dt.as("table")
      .merge(df1.as("input"), "table.day = input.day")
      .whenMatched()
      .updateExpr(
        Map(
          "product" -> "input.product",
          "store" -> "input.store",
          "sales" -> "input.sales",
        )
      )
      .whenNotMatched
      .insertAll
      .execute();
    dt
      .toDF
      .show()

    println("Time Travel in Delta Lake")
    dt
      .history()
      .show(true)

    println("Latest Version of data")
    sparkSession
      .read
      .format("delta")
      .load(args(0))
      .show()

    println("Version 0 of data")
    sparkSession
      .read
      .format("delta")
      .option("versionAsOf", 0)
      .load(args(0))
      .show()

    println("Stopping the spark session...")
    sparkSession.stop()
  }
}
