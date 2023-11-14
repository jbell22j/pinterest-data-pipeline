import requests
from time import sleep
import random
import json
import sqlalchemy
from sqlalchemy import text
import requests




random.seed(100)


class AWSDBConnector:

    '''
    This class is used to create a functional AWS database connector.

    Attributes:
        N/A
    '''

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

def run_infinite_post_data_loop():
    '''
    This function is send an infinite loop of data to API gateway.

    Parameters:
    N/A
    '''
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)
            headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
            pinload = json.dumps({
                "records": [
                    {
                        "value": {"index" : str(pin_result["index"]), "unique_id" : pin_result["unique_id"], "title" : pin_result["title"], "description" : pin_result["description"], "poster_name" : pin_result["poster_name"], "follower_count" : str(pin_result["follower_count"]), "tag_list" : pin_result["tag_list"], "is_image_or_video" : pin_result["is_image_or_video"], "image_src" : pin_result["image_src"], "downloaded" : str(pin_result["downloaded"]), "save_location" : pin_result["save_location"], "category" : pin_result["category"]}
                    }
                ]
            })
            res1 = requests.post("https://6jtmqzt94k.execute-api.us-east-1.amazonaws.com/test_stage/topics/0a65154c50dd.pin",headers=headers,data = pinload)
            

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)
            headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
            geoload = json.dumps({
                "records": [
                    {
                      "value": {"ind" : str(geo_result["ind"]), "timestamp" : str(geo_result["timestamp"]), "latitude" : str(geo_result["latitude"]), "longitude" : str(geo_result["longitude"]), "country" : geo_result["country"]}
                    }
                ]
            })
            res2 = requests.request("POST","https://6jtmqzt94k.execute-api.us-east-1.amazonaws.com/test_stage/topics/0a65154c50dd.geo",headers=headers,data = geoload)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
            headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
            userload = json.dumps({
                "records": [
                    {
                      "value": {"ind" : str(user_result["ind"]), "first_name" : user_result["first_name"], "last_name" : user_result["last_name"], "age" : str(user_result["age"]), "date_joined" : str(user_result["date_joined"])}
                    }
                ]
            })
            res3 = requests.request("POST","https://6jtmqzt94k.execute-api.us-east-1.amazonaws.com/test_stage/topics/0a65154c50dd.user",headers=headers,data = userload)
            
            print(f"Status code for pin results: {res1.status_code}")
            print(f"Status code for geo results: {res2.status_code}")
            print(f"Status code for user results: {res3.status_code}")
            
           


if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')
    
    


