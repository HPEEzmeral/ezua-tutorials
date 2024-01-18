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

    var sourceDF: DataFrame = null
    try {
      sourceDF = session.read.option("header", "true").format(srcFormat).load(srcPath)

      if (sourceDF == null || sourceDF.count() == 0) {
        throw new Exception("sourceDF is null after reading or has no rows")
      }
    } catch {
      case e: Exception => {
        println(s"Can not read from $srcPath: ${e.getMessage}")
        System.exit(1)
      }
    }
    println("Read complete")

    println("Processing data")
    var processedDf: DataFrame = null
    try {
      processedDf = processData(sourceDF)
    } catch {
      case e: Throwable => {
        e.printStackTrace()
        println(s"Can not process data: ${e.getMessage}")
        System.exit(1)
      }
    }
    println("Processing complete")

    println(s"Writing to $destPath; dest format is $destFormat")
    try{
      processedDf.write
        .format(destFormat)
        .option("header", "true")
        .mode(SaveMode.Overwrite)
        .save(destPath)
    } catch {
      case e: Exception => {
        println(s"Can not write to $destPath: ${e.getMessage}")
        System.exit(1)
      }
    }
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
