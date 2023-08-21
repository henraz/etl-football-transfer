from pyspark.sql import SparkSession


def start_spark(project_name:str) -> SparkSession:
    
    spark = (SparkSession
                .builder
                .appName(project_name)
                .getOrCreate())

    return spark