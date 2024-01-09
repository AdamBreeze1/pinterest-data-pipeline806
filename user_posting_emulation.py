import requests
from time import sleep
import random
import json
from sqlalchemy import text
from AWSDBConnector_creds import AWSDBConnector


random.seed(100)

new_connector = AWSDBConnector()

class PostToAWS:
    def convert_and_post(self, topic, selected_row):
        invoke_url = f"https://lly47uv1za.execute-api.us-east-1.amazonaws.com/beta/topics/{topic}"
        headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}

        for row in selected_row:
            result = dict(row._mapping)
            payload = json.dumps({
                "records": [
                    {"value": result}]
                    },
                        default=str)
            response = requests.request("POST", invoke_url, headers=headers, data=payload)
            print(payload)
            print(response)

    def run_infinite_post_data_loop(self):
        while True:
            sleep(random.randrange(0, 2))
            random_row = random.randint(0, 11000)
            engine = new_connector.create_db_connector()

            with engine.connect() as connection:

                # pin data
                pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
                pin_selected_row = connection.execute(pin_string)
                print("PIN")
                self.convert_and_post("0af85661a221.pin/", pin_selected_row)

                # geo data
                geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
                geo_selected_row = connection.execute(geo_string)
                print("GEO")
                self.convert_and_post("0af85661a221.geo/", geo_selected_row)

                # user data
                user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
                user_selected_row = connection.execute(user_string)
                print("USER")
                self.convert_and_post("0af85661a221.user/", user_selected_row)
                

if __name__ == "__main__":
    # First start the API Rest proxy
    new_post = PostToAWS()
    new_post.run_infinite_post_data_loop()
    print('Working')

