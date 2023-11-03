# Databricks notebook source
#Databricks code
#Reading the user dataframe
file_type = "json"
infer_schema = "true"

file_location_user = "/mnt/0a65154c50dd-mount/topics/0a65154c50dd.user/partition=0//*.json" 
df_user = spark.read.format(file_type) \
.option("inferSchema", infer_schema) \
.load(file_location_user)

display(df_user)
