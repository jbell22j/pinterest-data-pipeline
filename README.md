# pinterest-data-pipeline


## Project Brief

Pinterest crunches billions of data points every day to decide how to provide more value to their users. In this project we aimed to replicate the infrastructure utilized by Pinterest for the analysis of both historical and real-time data.

Pinterest boasts top-tier machine learning engineering systems, handling billions of daily user interactions like image uploads and clicks. In this project, I'm constructing a cloud-based system that processes these events through two distinct pipelines. One computes real-time metrics, like profile popularity for immediate recommendations, while the other calculates metrics relying on historical data, such as determining this year's most popular category.

<img width="651" alt="image" src="https://github.com/jbell22j/pinterest-data-pipeline/assets/141024595/210bf176-68d3-4128-bb2a-cb2ca111e84a">


### Project Dependencies

To execute this project, make sure to have the following modules installed:

* requests
* sqlalchemy

### Project Data

To simulate the data typically handled by Pinterest's engineers, the project includes a script called user_posting_emulation_to_console.py. When executed from the terminal, this script replicates the flow of random data points sent to the Pinterest API through POST requests as users upload data to the platform.

When the script is run, it initializes a database connector class responsible for establishing a connection to an AWS RDS database. This database comprises the following tables:

* `pinterest_data` contains data related to content being uploaded to Pinterest
* `geolocation_data` contains data related to the geolocation of each Pinterest post in `pinterest_data`
* `user_data contains` data related to the user whom each post in `pinterest_data` has been posted by

The `run_infinite_post_data_loop()` method continuously cycles at random intervals ranging from 0 to 2 seconds. During each iteration, it randomly selects all columns from a row in each of the three tables, compiling the data into a dictionary. Subsequently, these three dictionaries are printed to the console.

## Tools Used

* [Apache Kafka](https://kafka.apache.org/) - Apache Kafka is an open-source distributed event streaming platform. From the Kafka [documentation]:(https://kafka.apache.org/documentation/) Kafka combines three key capabilities so you can implement your use cases for event streaming end-to-end with a single battle-tested solution:

To publish (write) and subscribe to (read) streams of events, including continuous import/export of your data from other systems.
To store streams of events durably and reliably for as long as you want.
To process streams of events as they occur or retrospectively.
  
