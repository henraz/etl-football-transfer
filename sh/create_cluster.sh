#!/bin/bash

echo "------------------------ Create Cluster -----------------------------"

gcloud dataproc clusters create $1 \
--region us-central1 \
--zone "" \
--master-machine-type n2-standard-2 \
--master-boot-disk-size 200 \
--num-workers 2 \
--worker-machine-type n2-standard-2 \
--worker-boot-disk-size 500 \
--image-version 2.1-debian11 \
--max-idle 1200s \
--project $2