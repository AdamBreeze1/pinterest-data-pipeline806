import requests
import json


example_df = {"index": 1, "name": "Maya", "age": 25, "role": "engineer"}

# invoke url for one record, if you want to put more records replace record with records
invoke_url = f"https://lly47uv1za.execute-api.us-east-1.amazonaws.com/beta/streams/{stream_name}/record"

#To send JSON messages you need to follow this structure
payload = json.dumps({
    "StreamName": "YourStreamName",
    "Data": {
            #Data should be send as pairs of column_name:value, with different columns separated by commas      
            "index": example_df["index"], "name": example_df["name"], "age": example_df["age"], "role": example_df["role"]
            },
            "PartitionKey": "desired-name"
            })

headers = {'Content-Type': 'application/json'}

response = requests.request("PUT", invoke_url, headers=headers, data=payload)

print(response.status_code)

###########

def stream_posting(stream_name):
    # invoke url for one record, if you want to put more records replace record with records
    invoke_url = f"https://lly47uv1za.execute-api.us-east-1.amazonaws.com/beta/streams/{stream_name}/record"
    headers = {'Content-Type': 'application/json'}

    for row in selected_row:
            result = dict(row._mapping)
            payload = json.dumps({
                "records": [
                    {"value": result}]
                    },
                        default=str)
            response = requests.request("PUT", invoke_url, headers=headers, data=payload)

    print(response.status_code)

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


geo_stream_name = "streaming-0af85661a221-geo"
pin_stream_name = "streaming-0af85661a221-pin"
user_stream_name = "streaming-0af85661a221-user"