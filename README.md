# pinterest-data-pipeline

#### Table of Contents

- [Project Brief](#brief)
- [Project Dependencies](#dep)
- [Project Data](#data)
- [Tools Utilized](#tools)
- [Pipeline Architecture](#arc)
- [Building the Pipeline](#build)
- [Batch processing data using Apache Spark on Databricks](#batch)
- [Processing streaming data](#stream)

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
* `user_data` contains data related to the user whom each post in `pinterest_data` has been posted by

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

<a id="arc"></a>
## Pipeline Architecture

![CloudPinterestPipeline](https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/5e4d7a74-4d94-465c-bcb7-92b419440ba1)


 <a id="build"></a>
## Building the Pipeline

### Create an Apache cluster using AWS MSK

Our data pipeline begins with an Apache Kafka cluster within the AWS cloud ecosystem, utilizing Amazon Managed Streaming for Apache Kafka (MSK). The documentation provides a comprehensive guide for initiating the process, and I'll outline the steps taken to establish a functioning cluster here.

1. To begin, access the AWS console and locate MSK in the 'Services' menu.
2. Within the MSK menu, initiate the cluster creation process by selecting 'Create cluster.'
3. Opt for either the 'quick' or 'custom' create options, and assign a name to the cluster.

<img width="312" alt="image" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/c8721312-a5b9-4dd0-9f28-9718c6ad98bc"> 

4. Scroll down and select 'Provisioned,' specifying the Kafka version and broker type based on requirements and cost considerations.

<img width="324" alt="image" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/af8d34fc-3a45-47c2-8a97-e55b44615c7b">

5. Lastly, scroll down and hit 'Create cluster.' The creation process may take 15 to 20 minutes. Once done, go to the 'Properties' tab, find the network settings, and note the associated security group. Click 'View client information' and jot down the bootstrap servers.

### Create a client machine for the cluster

A client is needed to communicate with our configured cluster. In this project, an EC2 instance is employed to serve as the client.

1. Go to the EC2 dashboard and select 'Launch Instance.'

<img width="329" alt="image" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/fa5e83da-09e9-4425-942e-5e3d6a6addfc">

2. Provide a name for the instance, such as 'pinterest-kafka-client.'
3. Maintain the default Application and OS images, as well as the instance type, considering usage and cost considerations.
4. Generate a new keypair for secure SSH connection to the instance. Choose a descriptive name, select 'RSA,' and opt for '.pem' as the file format. The .pem file will download automatically; ensure its safekeeping for future use.

<img width="400" alt="image" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/5483ae4b-a439-401f-bf7d-955a67e74404">

5.Keep the default settings for the other sections. Click on 'Launch Instance'.

### Enable client machine to connect to the cluster

In order for the client machine to connect to the cluster, we need to edit the inbound rules for the security group associated with the cluster.

1. Within the EC2 menu on the left, access 'Security Groups.'

<img width="166" alt="image" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/e283c7d3-963e-469c-89fb-143f16c35642">

2. Pick the security group linked to the Kafka cluster (as identified earlier).
3. Navigate to the 'Inbound rules' tab, then click 'Edit inbound rules.'
4. Add a rule by selecting 'All traffic' for the type, and choose the security group linked to the EC2 instance.#
5. Save the rules.

We also need to create an IAM role for the client machine.

1. Go to the AWS IAM dashboard, choose 'Roles' from the left menu, and click 'Create role.'
2. Select 'AWS service' and 'EC2,' then proceed to the next step.
3. Choose 'Create policy' on the subsequent page.
4. In the policy editor, opt for JSON format and paste the provided policy. <strong> Note: This policy is somewhat open; a more restrictive policy is advisable for a production environment. </strong>

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "kafka:ListClustersV2",
                "kafka:ListVpcConnections",
                "kafka:DescribeClusterOperation",
                "kafka:GetCompatibleKafkaVersions",
                "kafka:ListClusters",
                "kafka:ListKafkaVersions",
                "kafka:GetBootstrapBrokers",
                "kafka:ListConfigurations",
                "kafka:DescribeClusterOperationV2"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "kafka-cluster:*",
            "Resource": [
                "arn:aws:kafka:*:<AWS-UUID>:transactional-id/*/*/*",
                "arn:aws:kafka:*:<AWS-UUID>:group/*/*/*",
                "arn:aws:kafka:*:<AWS-UUID>:topic/*/*/*",
                "arn:aws:kafka:*:<AWS-UUID>:cluster/*/*"
            ]
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": "kafka:*",
            "Resource": [
                "arn:aws:kafka:*:<AWS-UUID>:cluster/*/*",
                "arn:aws:kafka:*:<AWS-UUID>:configuration/*/*",
                "arn:aws:kafka:*:<AWS-UUID>:vpc-connection/*/*/*"
            ]
        }
    ]
}
```

5. On the subsequent page, provide a descriptive name for the policy and save it.
6. Return to the create role tab in the browser, refresh to display the new policy, and select it.
7. Proceed to the next step, give the role a descriptive name, and save the role.
8. In the EC2 dashboard, access the client instance.
9. Under 'Actions' and 'Security,' choose 'Modify IAM role.'
10. Pick the recently created role and click 'Update IAM role.'

### Install Kafka on the client machine

After the new instance is in the running state, establish an SSH connection to interact with the instance via the command line. To achieve this, click on the instance ID to open the summary page, then select 'Connect':

<img width="494" alt="connect-to-ec2" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/5505cb0e-330c-4f27-a9d8-652a8e203c5c">

Follow the instructions in the 'SSH' tab to connect to the instance.

```
# make sure key is not publicly viewable
chmod 400 pinterest-kafka-client-keypair.pem
# connect
ssh -i "pinterest-kafka-client-keypair.pem" ec2-user@<instance-public-DNS>
```

Now on the instance command line:

```
# install Java - required for Kafka to run
sudo yum install java-1.8.0
# download Kafka - must be same version as MSK cluster created earlier
wget https://archive.apache.org/dist/kafka/2.8.1/kafka_2.12-2.8.1.tgz
# unpack .tgz
tar -xzf kafka_2.12-2.8.1.tgz
```

Install the MSK IAM package that will enable the MSK cluster to authenticate the client:

```
# navigate to the correct directory
cd kafka_2.12-2.8.1/libs/
# download the package
wget https://github.com/aws/aws-msk-iam-auth/releases/download/v1.1.5/aws-msk-iam-auth-1.1.5-all.jar
```

Configure the client to be able to use the IAM package:

```
# open bash config file
nano ~/.bashrc
```

Add the following line to the config file, then save and exit:

```
export CLASSPATH=/home/ec2-user/kafka_2.12-2.8.1/libs/aws-msk-iam-auth-1.1.5-all.jar
```

Continue with configuration:

```
# activate changes to .bashrc
source ~/.bashrc
# navigate to Kafka bin folder
cd ../bin
# create client.properties file
nano client.properties
```

Add the following code to the client.properties file, then save and exit:

```
# Sets up TLS for encryption and SASL for authN.
security.protocol = SASL_SSL

# Identifies the SASL mechanism to use.
sasl.mechanism = AWS_MSK_IAM

# Binds SASL client implementation.
sasl.jaas.config = software.amazon.msk.auth.iam.IAMLoginModule required;

# Encapsulates constructing a SigV4 signature based on extracted credentials.
# The SASL client bound by "sasl.jaas.config" invokes this class.
sasl.client.callback.handler.class = software.amazon.msk.auth.iam.IAMClientCallbackHandler
```

### Create topics on the Kafka cluster

You can now generate topics on the Kafka cluster through the command line on the client machine. Employ the following command to create topics, utilizing the bootstrap server string documented earlier after the cluster creation.

```
<path-to-your-kafka-installation>/bin/kafka-topics.sh --create --bootstrap-server <BootstrapServerString> --command-config client.properties --topic <topic name>
```

In this project, I established three topics: one for `pinterest_data`, another for `geolocation_data`, and the last one for `user_data` as described earlier.

### Delivering messages to the Kafka cluster

With the cluster operational and the client configured to access and create topics, you can now employ the client to establish producers for streaming messages to the cluster and consumers for retrieving those messages. I utilized the Confluent package to establish a REST API on the client. This API listens for requests and interacts with the Kafka cluster accordingly.

To do this, first download the Confluent package to the client from the client's command line:

```
# download package
sudo wget https://packages.confluent.io/archive/7.2/confluent-7.2.0.tar.gz
# unpack .tar
tar -xvzf confluent-7.2.0.tar.gz
```

Modifying the kafka-rest.properties file next:

```
# navigate to the correct directory
cd cd confluent-7.2.0/etc/kafka-rest/
nano nano kafka-rest.properties
```

Update the `bootstrap.servers` and `zookeeper.connect` variables with the values obtained from the MSK cluster information. Integrate the following lines to enable authentication:

```
# Sets up TLS for encryption and SASL for authN.
client.security.protocol = SASL_SSL

# Identifies the SASL mechanism to use.
client.sasl.mechanism = AWS_MSK_IAM

# Binds SASL client implementation.
client.sasl.jaas.config = software.amazon.msk.auth.iam.IAMLoginModule required;

# Encapsulates constructing a SigV4 signature based on extracted credentials.
# The SASL client bound by "sasl.jaas.config" invokes this class.
client.sasl.client.callback.handler.class = software.amazon.msk.auth.iam.IAMClientCallbackHandler
```

The inbound rules for the client security group also need to be modified to allow incoming HTTP requests on port 8082. On the AWS 'Security groups' page, choose the security group attached to the client, and add the following inbound rule:

<img width="1820" alt="client-http-inbound-rules" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/92ec621f-3e10-4436-87e5-799187c21955">

To initiate the REST API, go to the confluent-7.2.0/bin directory and execute the following command:

```
./kafka-rest-start /home/ec2-user/confluent-7.2.0/etc/kafka-rest/kafka-rest.properties
```

Verify the API's request reception by opening a web browser and visiting "http://your-client-public-dns:8082/topics." The response should appear in the browser window and resemble something like:

```
["data.pin","data.geo","data.user"]
```

### AWS API Gateway

Access the AWS API Gateway service; a REST API is employed in this project.

1. Firstly, click 'Build' next to the REST API box:
<img width="629" alt="image" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/74c0b1ef-7e55-46b6-ada4-ae537b61e617">

2. Choose 'REST', 'New API', give the API a descriptive name, then click on 'Create API'.
3. From the 'Actions' menu, choose 'Create resource'. Select 'Configure as proxy resource' and 'Enable API Gateway CORS' boxes, then click on 'Create resource':
<img width="1459" alt="rest-api-create-resource" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/c6c57f8b-ab5b-48b5-91a1-139653c528a4">

4. On the next page, set up HTTP Proxy, using the address for earlier as the endpoint, "http://your-client-public-dns:8082/{proxy}".
5. With the resource and method created, it's possible to test the API (make sure that the REST proxy on the client is running and listening for requests). If everything is working correctly, the following test should result in a 200 response code and the same response body obtained through the browser.
<img width="846" alt="rest-api-test-method" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/e14fe6a8-3e39-4b22-a7f1-f1c4ae5eb01b">

6. Now the API needs to be deployed. From the 'Actions' menu, select 'Deploy API'. Choose 'New stage' and give the stage a name, then click on 'Deploy':
<img width="593" alt="rest-api-deploy" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/50878d19-7b1f-4c80-8ed0-6f8a98435ebe">

The process is now finished, and an invoke URL is generated for use in POST requests.

### Sending messages to the cluster using the API gateway

Executing the script `user_posting_emulation_batch_data.py` simulates a stream of messages, posting them to the cluster through the API gateway and Kafka REST proxy.
To access the messages in each topic within the cluster, I employed Kafka Connect, specifically AWS MSK Connect. This connection links the cluster to an AWS S3 bucket, serving as a repository for deposited messages.

### Connecting the Apache cluster to AWS S3 bucket

To begin, establish an S3 bucket that will be linked to the cluster.

1. On the AWS S3 dashboard, choose 'Create bucket.
2. Assign a unique and descriptive name to the bucket, ensuring it is in the same AWS region as other project resources. Maintain default settings for other configurations.
Now, proceed to create an IAM role for the MSK connector, utilizing the following policy. Note that this policy might not be sufficiently restrictive for production; its usage is confined to development purposes only.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "kafka-cluster:DescribeCluster",
                "kafka-cluster:Connect"
            ],
            "Resource": [
                "arn:aws:s3:::<BUCKET-NAME>",
                "arn:aws:s3:::<BUCKET-NAME>/*",
                "arn:aws:kafka:<REGION>:<AWS-UUID>:cluster/<CLUSTER-NAME>/<CLUSTER-UUID>"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:ReadData",
                "kafka-cluster:DescribeTopic"
            ],
            "Resource": "arn:aws:kafka:<REGION>:<AWS-UUID>:topic/<CLUSTER-NAME>/<CLUSTER-UUID>/*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:DescribeTopic",
                "kafka-cluster:WriteData"
            ],
            "Resource": "arn:aws:kafka:<REGION>:<AWS-UUID>:topic/<CLUSTER-NAME>/<CLUSTER-UUID>/*"
        },
        {
            "Sid": "VisualEditor3",
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:CreateTopic",
                "kafka-cluster:ReadData",
                "kafka-cluster:DescribeTopic",
                "kafka-cluster:WriteData"
            ],
            "Resource": "arn:aws:kafka:<REGION>:<AWS-UUID>:topic/<CLUSTER-NAME>/<CLUSTER-UUID>/__amazon_msk_connect_*"
        },
        {
            "Sid": "VisualEditor4",
            "Effect": "Allow",
            "Action": [
                "kafka-cluster:AlterGroup",
                "kafka-cluster:DescribeGroup"
            ],
            "Resource": [
                "arn:aws:kafka:<REGION>:<AWS-UUID>:group/<CLUSTER-NAME>/<CLUSTER-UUID>/__amazon_msk_connect_*",
                "arn:aws:kafka:<REGION>:<AWS-UUID>:group/<CLUSTER-NAME>/<CLUSTER-UUID>/connect-*"
            ]
        },
        {
            "Sid": "VisualEditor5",
            "Effect": "Allow",
            "Action": [
                "s3:ListStorageLensConfigurations",
                "s3:ListAccessPointsForObjectLambda",
                "s3:GetAccessPoint",
                "s3:PutAccountPublicAccessBlock",
                "s3:GetAccountPublicAccessBlock",
                "s3:ListAllMyBuckets",
                "s3:ListAccessPoints",
                "s3:PutAccessPointPublicAccessBlock",
                "s3:ListJobs",
                "s3:PutStorageLensConfiguration",
                "s3:ListMultiRegionAccessPoints",
                "s3:CreateJob"
            ],
            "Resource": "*"
        }
    ]
}
```
The role should have the following trust relationship:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "kafkaconnect.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

The subsequent task involves establishing a VPC endpoint to S3.

1. In the AWS VPC dashboard, opt for 'Endpoints' from the left-hand menu, and then click 'Create endpoint.'
2. Provide a descriptive name for the endpoint.
3. Select 'AWS services.'
4. In the 'Services' search field, look for 'S3.'
5. Choose:

<img width="1819" alt="vpc-endpoint" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/1a13b450-5d5c-4c49-a7a0-0dad9eb6c3ac">

Select the default VPC corresponding to the region, mark the checkbox beside the default route tables, and proceed to click 'Create endpoint.'

Now, let's proceed to create the connector. The initial step involves establishing a new plugin for the connector.

1. To craft the plugin, you'll need a .zip file containing the plugin files. For the Kafka S3 Sink Connector, download it from "https://www.confluent.io/hub/confluentinc/kafka-connect-s3." After downloading, upload it to the S3 bucket, either via the console or a web browser.
2. In the AWS MSK dashboard, choose 'Custom plugins' from the left-hand menu, and then click 'Create custom plugin.'
3. In the subsequent window, navigate to the S3 bucket housing the .zip file, and select the .zip file:

<img width="817" alt="custom-plugin" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/a5b63663-516f-426c-8807-05177480da42">

4. Select 'Create custom plugin.' The procedure will require a few minutes.
5. Next, establish the connector by going to 'Connectors' in the MSK dashboard's left-hand menu.
6. Choose 'Create connector.'
7. Opt for 'Use existing plugin' and designate the recently created plugin. Proceed by clicking 'Next.'
8. Assign a name to the connector, ensure 'MSK cluster' is highlighted, and then select the earlier created cluster.
9. Apply the subsequent settings for configuration:
```
connector.class=io.confluent.connect.s3.S3SinkConnector
# same region as our bucket and cluster
s3.region=<REGION>
flush.size=1
schema.compatibility=NONE
tasks.max=3
# this depends on names given to topics
topics.regex=<TOPIC-NAME>.*
format.class=io.confluent.connect.s3.format.json.JsonFormat
partitioner.class=io.confluent.connect.storage.partitioner.DefaultPartitioner
value.converter.schemas.enable=false
value.converter=org.apache.kafka.connect.json.JsonConverter
storage.class=io.confluent.connect.s3.storage.S3Storage
key.converter=org.apache.kafka.connect.storage.StringConverter
s3.bucket.name=<BUCKET_NAME>
```

10. Opt for defaults in the remaining settings until 'Access Permissions,' where the IAM role designated for the connector must be selected.
11. Click 'Next,' followed by 'Next' once more. Choose a location for log delivery; I opted to have logs delivered to the S3 bucket.
12. Proceed by clicking 'Next' and then 'Create connector.'

After the completion of the connector creation process, you should observe any messages sent to the cluster within the S3 bucket, organized in a folder titled 'Topics.'


 <a id="batch"></a>
## Batch processing data using Apache Spark on Databricks

To facilitate batch processing of data on Databricks, it's crucial to establish a mount for the S3 bucket on the platform. The notebook `mount_s3_bucket.ipynb`, executed on the Databricks platform, encompasses the following steps:

1. Import necessary libraries
2. List tables in Databricks filestore in order to obtain AWS credentials file name
3. Read the credentials .csv into a Spark dataframe
4. Generate credential variables from Spark dataframe
5. Mount the S3 bucket containing the messages from the Kafka topics
6. List the topics
7. Read the .json message files into three Spark dataframes, one each for each of the topics
8. Unmount the S3 bucket

### Clean and query data using Apache Spark on Databricks

The file databricks_data_cleaning_and_sql_notebook.ipynb contains the code for performing the necessary cleaning of the dataframes created using the steps above and the querying and returning specific insights about the data of the subsequent clean dataframes.

### Orchestrating automated workflow of notebook on Databricks

MWAA was employed to automate the execution of batch processing on Databricks. The Python code file `0a65154c50dd_dag.py` constitutes a Directed Acyclic Graph (DAG) orchestrating the execution of the aforementioned batch processing notebook. Uploaded to the MWAA environment, Airflow within MWAA is utilized to establish connections and execute the Databricks notebook at scheduled intervals, specified here as `@daily`.

### Data Tables

The geolocation data as an example looks like this after cleaning:
<img width="387" alt="image" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/0bfec375-94c2-4668-9f4f-c1f3f083d1fe">

 <a id="stream"></a>
## Processing streaming data

### Create data streams on Kinesis

Initiating the processing of streaming data involved the creation of three streams on AWS Kinesis, each dedicated to a distinct data source.

1. From the Kinesis dashboard, select 'Create data stream'.
2. Give the stream a name, and select 'Provisioned' capacity mode.
3. Click on 'Create data stream' to complete the process.

### Create API proxy for uploading data to streams

Interacting with the recently added Kinesis streams through HTTP requests is achievable. To enable this, I established new API resources on AWS API Gateway.

For the DELETE method, the configured settings were:
* 'Integration Type': 'AWS Service'
* 'AWS Region': 'us-east-1'
* 'AWS Service': 'Kinesis'
* 'HTTP method': 'POST'
* 'Action': 'DeleteStream'
* 'Execution role': 'ARN of the created IAM role'

In 'Integration Request' under 'HTTP Headers', add a new header:

'Name': 'Content-Type'
'Mapped from': 'application/x-amz-json-1.1'
Under 'Mapping Templates', add new mapping template:

'Content Type': 'application/json'
Use the following code in the template:
```
{
    "StreamName": "$input.params('stream-name')"
}
```

<img width="1210" alt="delete-method-settings-2" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/3994e3c9-4388-4941-822d-bea76435cbc9">

For the other methods, the same settings were used except for:

* GET
'Action': 'DescribeStream'
'Mapping Template':
```
{
    "StreamName": "$input.params('stream-name')"
}
```
* POST
  'Action': 'CreateStream'
  'Mapping Template':
```
{
    "ShardCount": #if($input.path('$.ShardCount') == '') 5 #else $input.path('$.ShardCount') #end,
    "StreamName": "$input.params('stream-name')"
}
```
/record

*PUT
'Action': 'PutRecord'
'Mapping Template':
```
{
    "StreamName": "$input.params('stream-name')",
    "Data": "$util.base64Encode($input.json('$.Data'))",
    "PartitionKey": "$input.path('$.PartitionKey')"
}
```
/records

* PUT
'Action': 'PutRecords'
'Mapping Template':
```
{
    "StreamName": "$input.params('stream-name')",
    "Records": [
       #foreach($elem in $input.path('$.records'))
          {
            "Data": "$util.base64Encode($elem.data)",
            "PartitionKey": "$elem.partition-key"
          }#if($foreach.hasNext),#end
        #end
    ]
}
```
After creating the new resources and methods, the API must be redeployed.

### Sending data to the Kinesis streams

Executing the script `user_posting_emulation_streaming.py` initiates an infinite loop. Similar to the examples mentioned earlier, it fetches records from the RDS database and transmits them through the new API to Kinesis.

### Processing the streaming data in Databricks

The Jupyter notebook `data_streaming_and_cleaning_from_kinesis.ipynb` encompasses all the essential code for fetching the streams from Kinesis, refining (cleaning) the data, and subsequently loading the data into Delta tables on the Databricks cluster.






















