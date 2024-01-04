# pinterest-data-pipeline

#### Table of Contents

- [Project Brief](#brief)
- [Project Dependencies](#dep)
- [Project Data](#data)
- [Tools Utilized](#tools)
- [Building the Pipeline](#build)

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
