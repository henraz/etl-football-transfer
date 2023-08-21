import os, json
from pyspark import SparkFiles

def open_config_json(prefix_file_name:str) -> dict:


    file_name = f"{prefix_file_name}_config.json"

    root_file = SparkFiles.getRootDirectory()
    absolute_file_path = os.path.join(root_file, file_name)

    file = open(absolute_file_path)
    load_file = json.load(file)
    return load_file