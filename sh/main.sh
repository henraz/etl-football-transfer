#!/bin/bash

PROJECT_ID="project-dev"
CLUSTER_NAME="football-transfer"


PYSPARK_JOB="./src/elt_football_transfer.py"
CONFIG_FILE="./configs/etl_football_transfer_config.json"
PROJECT_WHL="./dist/etl_football_transfer-0.0.1-py3-none-any.whl"

# Create Dataproc Cluster
CREATE_CLUSTER="./sh/create_cluster.sh"
source "$CREATE_CLUSTER" $CLUSTER_NAME $PROJECT_ID

# Submit Pyspark job
SUBMIT_PYSPARK="./sh/submit_pyspark.sh"
source "$SUBMIT_PYSPARK" $CLUSTER_NAME $PYSPARK_JOB "--py-files=$PROJECT_WHL,$CONFIG_FILE"