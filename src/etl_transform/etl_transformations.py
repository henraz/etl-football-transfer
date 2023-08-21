from pyspark.sql.types import DoubleType
from pyspark.sql import DataFrame
import pyspark.sql.functions as f
import utils.bq_module as bq


def clean_data(df:DataFrame) -> DataFrame:

    df = df.withColumn("fee_description", \
                      f.when(((df.fee) == "-") | ((df.fee) == "?"), "NA")
                      .otherwise(df.fee)) \
                      .drop(df.fee)
  
    df = df.withColumn("fee", \
                         f.when(df.fee_cleaned == "NA", None)
                         .otherwise(df.fee_cleaned)
                      )  \
                     .withColumn("fee", f.col("fee").cast(DoubleType())) \
                     .drop(df.fee_cleaned)
    return df


def create_dim(df_source:DataFrame, dict_dim:dict) -> dict:
   
   dict_df_dim = {}

   for key, value in dict_dim.items():
      df = df_source
      df = df.select(value[1:]).distinct()
      df = df.withColumn(value[0], f.monotonically_increasing_id()) \
             .select(value)
      
      dict_df_dim[key] = df
      
   return dict_df_dim


def create_fact(df_source:DataFrame, dict_df_dim:dict, dict_dim:dict, dict_fact:dict) -> DataFrame:

    df_fact = df_source
    for key, value in dict_df_dim.items():
        df_fact = df_fact.join(value, dict_dim[key][1:], "inner")

    fact_name = [*dict_fact][0]
    fact_columns = dict_fact[fact_name]
    df_fact = df_fact.select(fact_columns)

    return df_fact


def save_dim_fact_bq(df_fact:DataFrame, dict_df_dim:dict, dict_target:dict) -> None:

    for key, value in dict_df_dim.items():
        bq.write_bq(value, dict_target, key)

    dict_fact = dict_target['fact']
    fact_name = [*dict_fact][0]

    bq.write_bq(df_fact, dict_target, fact_name)