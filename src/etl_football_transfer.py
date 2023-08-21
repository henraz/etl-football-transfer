from utils.spark_module import start_spark
import utils.gcs_module as gcs
import utils.aux_module as aux
import etl_transform.etl_transformations as trf


def main():

    # Start Spark Session
    spark = start_spark("etl_football_transfer")

    # Config file
    config = aux.open_config_json('etl_football_transfer')
    dict_info_source = config["source"]
    dict_info_target = config["target"]
    dict_dimensions = dict_info_target["dimensions"]
    dict_fact = dict_info_target["fact"]

    # Temporary Bucket
    temporary_bucket = dict_info_target["temporary_bucket"]
    spark.conf.set('temporaryGcsBucket', temporary_bucket)

    # Source
    blobs_list = gcs.list_blobs_name(dict_info_source)

    df_source = gcs.read_csv(spark, dict_info_source, blobs_list[0])
    
    for i in range(1, len(blobs_list)):
       df_new = gcs.read_csv(spark, dict_info_source, blobs_list[i])
       df_source = df_source.union(df_new)

    # Cleaning Source
    df_source = trf.clean_data(df_source)

    # Dimensions
    dict_df_dimensions = trf.create_dim(df_source, dict_dimensions)
    
    # Fact
    df_fact = trf.create_fact(df_source, dict_df_dimensions, dict_dimensions, dict_fact)
    
    # Write tables BQ
    trf.save_dim_fact_bq(df_fact, dict_df_dimensions, dict_info_target)


if __name__== '__main__':
    main()