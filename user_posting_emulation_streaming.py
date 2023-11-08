import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text
import requests




random.seed(100)


class AWSDBConnector:

    def __init__(self):

        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()

def run_infinite_stream_data_loop():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)
            headers = {'Content-Type': 'application/json'}
            pinload = json.dumps({
                "StreamName": "streaming-0a65154c50dd-pin",
                "Data": 
                    {
                        "index" : str(pin_result["index"]), "unique_id" : pin_result["unique_id"], "title" : pin_result["title"], "description" : pin_result["description"], "poster_name" : pin_result["poster_name"], "follower_count" : str(pin_result["follower_count"]), "tag_list" : pin_result["tag_list"], "is_image_or_video" : pin_result["is_image_or_video"], "image_src" : pin_result["image_src"], "downloaded" : str(pin_result["downloaded"]), "save_location" : pin_result["save_location"], "category" : pin_result["category"]
                    },
                "PartitionKey": "partition-1"
                
            })
            res1 = requests.request("PUT","https://6jtmqzt94k.execute-api.us-east-1.amazonaws.com/test_stage/streams/streaming-0a65154c50dd-pin/record",headers=headers,data = pinload)
            

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)
            headers = {'Content-Type': 'application/json'}
            geoload = json.dumps({
                "StreamName": "streaming-0a65154c50dd-geo",
                "Data": 
                    {
                      "index" : str(geo_result["ind"]), "timestamp" : str(geo_result["timestamp"]), "latitude" : str(geo_result["latitude"]), "longitude" : str(geo_result["longitude"]), "country" : geo_result["country"]
                    },
                "PartitionKey": "partition-2"
            })
            res2 = requests.request("PUT","https://6jtmqzt94k.execute-api.us-east-1.amazonaws.com/test_stage/streams/streaming-0a65154c50dd-geo/record",headers=headers,data = geoload)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
            headers = {'Content-Type': 'application/json'}
            userload = json.dumps({
                "StreamName": "streaming-0a65154c50dd-geo",
                "Data": {
                "index" : str(user_result["ind"]), "first_name" : user_result["first_name"], "last_name" : user_result["last_name"], "age" : str(user_result["age"]), "date_joined" : str(user_result["date_joined"])
                },
                "PartitionKey": "partition-3"
            })
            res3 = requests.request("PUT","https://6jtmqzt94k.execute-api.us-east-1.amazonaws.com/test_stage/streams/streaming-0a65154c50dd-user/record",headers=headers,data = userload)
            
            print(f"Status code for pin results: {res1.status_code}")
            print(f"Status code for geo results: {res2.status_code}")
            print(f"Status code for user results: {res3.status_code}")
            
           


if __name__ == "__main__":
    run_infinite_stream_data_loop()
    print('Working')