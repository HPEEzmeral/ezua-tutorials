ThisBuild / scalaVersion := "2.12.18"
ThisBuild / organization := "com.mapr.sparkdemo"
ThisBuild / version      := "1.0.0"

lazy val dataProcessTransfer = project
  .in(file("."))
  .settings(
    name := "DataProcessTransfer",
    assembly / assemblyOutputPath := file("DataProcessTransfer.jar"),
    libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.5.0" % "provided"
  )
