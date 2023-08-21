from google.cloud import storage
from pyspark.sql import DataFrame, SparkSession

def list_blobs_name(dict_info:dict) -> list:
    
    list_blobs = []
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(dict_info["bucket"], prefix = dict_info["folder"])
    for blob in blobs:
        if blob.name[-4:] == ".csv":
            list_blobs.append(blob.name)

    return list_blobs


def read_csv(spark:SparkSession, dict_info:dict, file:str) -> DataFrame:
    
    bucket_name = dict_info["bucket"]
    header  = dict_info["header"]
    delimiter = dict_info["delimiter"]
    path_file = f'gs://{bucket_name}/{file}'

    df = (spark.read.format("csv")
                .option("header", header)
                .option("delimiter", delimiter)
                .load(path_file))
    
    return df

 
def write_csv(df:DataFrame, dict_info:dict) -> None:
    
    
    bucket_name = dict_info["bucket"]
    path = dict_info["caminho"]
    mode = dict_info["modo"]

    df.write.format("csv") \
        .mode(mode) \
        .save(f"gs://{bucket_name}/{path}")