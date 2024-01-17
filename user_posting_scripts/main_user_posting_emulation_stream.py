import random
import requests
import json

from database_utils import *


new_connector = AWSDBConnector()

@just_keep_running
def start_receiving_post_data_streaming():
    # post the data records to the invoke url and receive a response to confirm if successful
    # sends to aws S3 for storage
    headers = {'Content-Type': 'application/json'}
    invoke_subdirectory = "https://lly47uv1za.execute-api.us-east-1.amazonaws.com/beta/streams/"
    pin_invoke_url = f"{invoke_subdirectory}streaming-0af85661a221-pin/record"
    geo_invoke_url = f"{invoke_subdirectory}streaming-0af85661a221-geo/record"
    user_invoke_url = f"{invoke_subdirectory}streaming-0af85661a221-user/record"

    # generate a random row number between 0 and 11000
    random_row = random.randint(0, 11000)
    # get the data for the random_row of each table
    pin_data = new_connector.get_records("pinterest_data", random_row)
    geo_data = new_connector.get_records("geolocation_data", random_row)
    user_data = new_connector.get_records("user_data", random_row)

    # pin posting
    pin_payload = json.dumps({
        "StreamName": "streaming-0af85661a221-pin",
        "Data": pin_data,
        "PartitionKey": "0af85661a221_PartitionKey"
            },
                default=str)               
    pin_response = requests.request("PUT", pin_invoke_url, headers=headers, data=pin_payload)
    print(pin_response)

    # geo posting
    geo_payload = json.dumps({
        "StreamName": "streaming-0af85661a221-geo",
        "Data": geo_data,
        "PartitionKey": "0af85661a221_PartitionKey"
            },
                default=str)               
    geo_response = requests.request("PUT", geo_invoke_url, headers=headers, data=geo_payload)
    print(geo_response)

    # user posting
    user_payload = json.dumps({
        "StreamName": "streaming-0af85661a221-user",
        "Data": user_data,
        "PartitionKey": "0af85661a221_PartitionKey"
            },
                default=str)               
    user_response = requests.request("PUT", user_invoke_url, headers=headers, data=user_payload)
    print(user_response)

if __name__ == "__main__":
    print('Working...')
    start_receiving_post_data_streaming()
