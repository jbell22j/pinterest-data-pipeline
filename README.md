# pinterest-data-pipeline

#### Table of Contents

- [Project Brief](#brief)
- [Project Dependencies](#dep)
- [Project Data](#data)
- [Tools Utilized](#tools)

 <a id="brief"></a>
## Project Brief 

Pinterest crunches billions of data points every day to decide how to provide more value to their users. In this project we aimed to replicate the infrastructure utilized by Pinterest for the analysis of both historical and real-time data.

Pinterest boasts top-tier machine learning engineering systems, handling billions of daily user interactions like image uploads and clicks. In this project, I'm constructing a cloud-based system that processes these events through two distinct pipelines. One computes real-time metrics, like profile popularity for immediate recommendations, while the other calculates metrics relying on historical data, such as determining this year's most popular category.

<img width="855" alt="image" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/759369bf-703c-4aff-b45d-a8585db1a4c7">


 <a id="dep"></a>
## Project Dependencies

To execute this project, make sure to have the following modules installed:

* requests
* sqlalchemy

 <a id="data"></a>
## Project Data 

To simulate the data typically handled by Pinterest's engineers, the project includes a script called user_posting_emulation_to_console.py. When executed from the terminal, this script replicates the flow of random data points sent to the Pinterest API through POST requests as users upload data to the platform.

When the script is run, it initializes a database connector class responsible for establishing a connection to an AWS RDS database. This database comprises the following tables:

* `pinterest_data` contains data related to content being uploaded to Pinterest
* `geolocation_data` contains data related to the geolocation of each Pinterest post in `pinterest_data`
* `user_data contains` data related to the user whom each post in `pinterest_data` has been posted by

The `run_infinite_post_data_loop()` method continuously cycles at random intervals ranging from 0 to 2 seconds. During each iteration, it randomly selects all columns from a row in each of the three tables, compiling the data into a dictionary. Subsequently, these three dictionaries are printed to the console.

 <a id="tools"></a>
## Tools Utilized 

* [Apache Kafka](https://kafka.apache.org/) - Apache Kafka is an open-source distributed event streaming platform. From the Kafka [documentation](https://kafka.apache.org/documentation/):
> Event streaming is the practice of capturing data in real-time from event sources like databases, sensors, mobile devices, cloud services, and software applications in the form of streams of events; storing these event streams durably for later retrieval; manipulating, processing, and reacting to the event streams in real-time as well as retrospectively; and routing the event streams to different destination technologies as needed. Kafka combines three key capabilities so you can implement your use cases for event streaming end-to-end with a single battle-tested solution. Kafka is a distributed system consisting of servers and clients that communicate via a high-performance TCP network protocol.
* [Apache Spark](https://spark.apache.org/docs/3.4.1/) - Apache Spark™ is a multi-language engine for executing data engineering, data science, and machine learning on single-node machines or clusters.
* [AWS API Gateway](https://aws.amazon.com/api-gateway/) - Amazon API Gateway, an AWS service, facilitates the creation, publishing, maintenance, monitoring, and securing of REST, HTTP, and WebSocket APIs at any scale. API developers can design APIs that interact with AWS or other web services, along with data stored in the AWS Cloud.
* [AWS Kinesis](https://aws.amazon.com/kinesis/) - AWS Kinesis is a managed service designed for the processing and analysis of streaming data. In this project, I've employed Kinesis Data Streams to gather and temporarily store data before utilizing Spark on Databricks to read and process the stream.
* [AWS MSK](https://aws.amazon.com/msk/) - Amazon Managed Streaming for Apache Kafka (MSK) enables secure data streaming through a fully managed and highly available Apache Kafka service. For further details, refer to the [developer guide](https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html).
* [AWS MSK Connect](https://docs.aws.amazon.com/msk/latest/developerguide/msk-connect.html) - AWS MSK Connect simplifies the process for developers to stream data to and from their Apache Kafka clusters.
* [Databricks](https://docs.databricks.com/en/index.html) - In this project, the Databricks platform is utilized for Spark processing of both batch and streaming data. From the [documentation](https://docs.databricks.com/en/introduction/index.html):
> Databricks is a unified, open analytics platform for building, deploying, sharing, and maintaining enterprise-grade data, analytics, and AI solutions at scale. The Databricks Data Intelligence Platform integrates with cloud storage and security in your cloud account, and manages and deploys cloud infrastructure on your behalf.
* [PySpark](https://spark.apache.org/docs/3.4.1/api/python/index.html) - PySpark is the Python API for Apache Spark. From the [documentation]:
> It enables you to perform real-time, large-scale data processing in a distributed environment using Python. It also provides a PySpark shell for interactively analyzing your data. PySpark combines Python’s learnability and ease of use with the power of Apache Spark to enable processing and analysis of data at any size for everyone familiar with Python. PySpark supports all of Spark’s features such as Spark SQL, DataFrames, Structured Streaming, Machine Learning (MLlib) and Spark Core.
* [Kafka REST Proxy](https://docs.confluent.io/platform/current/kafka-rest/index.html) - From the [documentation](https://docs.confluent.io/platform/current/kafka-rest/index.html):
> The Confluent REST Proxy provides a RESTful interface to an Apache Kafka® cluster, making it easy to produce and consume messages, view the state of the cluster, and perform administrative actions without using the native Kafka protocol or clients.
* [Managed Workflows for Apache Airflow](https://docs.aws.amazon.com/mwaa/latest/userguide/what-is-mwaa.html) - With Apache Airflow, users can employ Python to construct scheduling workflows for batch-oriented processes. In this project, MWAA is leveraged to orchestrate batch processing on the Databricks platform.
