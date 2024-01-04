# pinterest-data-pipeline


## Project Brief

Pinterest crunches billions of data points every day to decide how to provide more value to their users. In this project we aimed to replicate the infrastructure utilized by Pinterest for the analysis of both historical and real-time data.

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
