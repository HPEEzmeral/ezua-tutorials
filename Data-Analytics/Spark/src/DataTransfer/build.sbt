ThisBuild / scalaVersion := "2.12.18"
ThisBuild / organization := "com.mapr.sparkdemo"
ThisBuild / version      := "1.0.0"

lazy val dataTransfer = project
  .in(file("."))
  .settings(
    name := "DataTransfer",
    assembly / assemblyOutputPath := file("DataTransfer.jar"),
    libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.5.0" % "provided"
  )
