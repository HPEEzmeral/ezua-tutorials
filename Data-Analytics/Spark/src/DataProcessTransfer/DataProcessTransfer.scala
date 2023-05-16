package com.mapr.sparkdemo

import org.apache.spark.sql.{SaveMode, SparkSession}
import org.apache.spark.sql.functions.col
import org.apache.spark.sql.DataFrame

import scala.reflect.io.Directory

import java.io.File
import java.nio.file.{Paths, Files, Path, StandardCopyOption}


object DataProcessTransfer {
  def main(args: Array[String]): Unit = {
    if (args.length != 4) {
      printUsage()
      System.exit(1)
    }

    val srcPath = args(0)
    val srcFormat = args(1)
    val destPath = args(2)
    val destFormat = args(3)

    validateDestinationPath(destPath)

    val session = SparkSession.builder().getOrCreate()

    println(s"Reading from $srcPath; src format is $srcFormat")
    val sourceDF = session.read.option("header", "true").format(srcFormat).load(srcPath)
    println("Read complete")

    val processedDf = processData(sourceDF)

    println(s"Writing to $destPath; dest format is $destFormat")
    processedDf.write
      .format(destFormat)
      .option("header", "true")
      .mode(SaveMode.Overwrite)
      .save(destPath)
    println("Write complete")

    session.stop()
  }

  private def printUsage(): Unit = {
    println(
      """App expects exactly 4 arguments:
        |- source path
        |- source format
        |- destination path
        |- destination format
        |""".stripMargin)
  }

  private def processData(df: DataFrame): DataFrame = {
    def increment(df: DataFrame): DataFrame = df.select(df.columns.map(c => (col(c) + 1).alias(c)): _*)
    increment(df)
  }

  private def validateDestinationPath(destPath: String): Unit = {
    val internalFsMode = "file://"
    if (!(destPath.contains(internalFsMode))) {
      println(s"Can not write to PV. Destination path is not '$internalFsMode'")
      System.exit(1)
    }
  }
}
