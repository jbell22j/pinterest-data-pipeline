# Databricks notebook source
#Databricks code
#Reading the geo dataframe
file_type = "json"
infer_schema = "true"

file_location_geo = "/mnt/0a65154c50dd-mount/topics/0a65154c50dd.geo/partition=0//*.json" 
df_geo = spark.read.format(file_type) \
.option("inferSchema", infer_schema) \
.load(file_location_geo)

display(df_geo)
