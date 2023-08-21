from google.cloud import bigquery
from pyspark.sql import DataFrame

def write_bq(df:DataFrame, dict_info:dict, table_name:str):

    project_id = dict_info["project_id"] 
    dataset    = dict_info["dataset"]
    mode_write = dict_info["mode_write"]

    path = f"{project_id}.{dataset}.{table_name}"

    df.write.format('bigquery') \
        .option('table', path) \
        .mode(mode_write) \
        .save()