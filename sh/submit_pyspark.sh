#!/bin/bash

echo "------------------------ Start pyspark job --------------------------"

gcloud dataproc jobs submit pyspark \
--cluster=$1 \
--region=us-central1 $2 $3 \
--jars=gs://spark-lib/bigquery/spark-bigquery-latest.jar
