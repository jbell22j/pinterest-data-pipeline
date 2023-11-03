# Databricks notebook source
#Reading the pin dataframe
file_type = "json"
infer_schema = "true"

file_location_pin = "/mnt/0a65154c50dd-mount/topics/0a65154c50dd.pin/partition=0//*.json" 
df_pin = spark.read.format(file_type) \
.option("inferSchema", infer_schema) \
.load(file_location_pin)

display(df_pin)


