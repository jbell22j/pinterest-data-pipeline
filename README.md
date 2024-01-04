# pinterest-data-pipeline


## Project Goals

### Aims

Pinterest crunches billions of data points every day to decide how to provide more value to their users. In this project we aimed to replicate the infrastructure utilized by Pinterest for the analysis of both historical and real-time data.

### Outcomes

This project has taught me how to use AWS cloud in detail, extracting data from databases stored on AWS, sending relevant data via. batch and streaming methods (AWS kinesis, s3-bucket, API Gateway, MWAA). Extending this cloud system through Databricks cleaning the data and querying it using SQL commands via PySpark.

## Usage Instructions

### Project Dependencies

To execute this project, make sure to have the following modules installed:

* requests
* sqlalchemy

### Batch Data

- Configure an EC2 kafka client
- Connect an MSK cluster to an S3-bucket
- Configure an API in API gateway

Make sure to change API endpoint URL in the 'user_posting_emulation.py' file to the names you have created now in your own AWS account.

### Streaming Data

USE REGION US-EAST-1 FOR EASE IN AWS

'user_posting_emulation_streaming.py' requires you to create your own three data streams in AWS Kinesis for the three databases, 'pin', 'user' and 'geo', you then change the 'StreamName' variables in a copy of the file in your Visual Studio Code/Python to the names of the streams in your AWS Kinesis. Configure a REST API to allow it to invoke Kinesis actions. You will need to create an IAM role for your API to access Kinesis.

Your API should be able to invoke the following actions:

- List streams in Kinesis
- Create, describe and delete streams in Kinesis
- Add records to streams in Kinesis

Then change the API link to the add record to streams in Kinesis link you have just configured and the data should stream to your Kinesis streams when you run the file.

In Databricks, you will need to create an authorisation credentials file for your AWS account and replace named 'authorisation_credentials.csv' to retrieve your access key and secret access key. Run your preferred method to ingest data into Kinesis Data Streams. In the Kinesis console, check your data streams are receiving the data. The rest of the file should run smoothly, just make sure to change the names for your Delta tables and stream names.

## File Structure

'user_posting_emulation.py' BATCH DATA EXTRACTION AND UPLOAD FROM / TO AWS
'user_posting_emulation_streaming.py' STREAMING DATA EXTRACTION AND UPLOAD FROM / TO AWS

All of the .ipynb are files created in Databricks, to clean and query the data.
'0a65154c50dd_dag.py' file is used to systematically run the Databricks file 'databrickes_data_cleaning_and_sql_queries_notebook.ipynb' file to clean and query the pinterest data in batches.
