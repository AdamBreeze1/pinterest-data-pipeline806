import random
import requests
import json

from database_utils import *


new_connector = AWSDBConnector()

@just_keep_running
def start_receiving_post_data_batch():
    # post the data records to the invoke url and receive a response to confirm if successful
    # sends to aws S3 for storage
    headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
    invoke_subdir = "https://lly47uv1za.execute-api.us-east-1.amazonaws.com/beta/topics/"
    pin_invoke_url = f"{invoke_subdir}0af85661a221.pin/"
    geo_invoke_url = f"{invoke_subdir}0af85661a221.geo/"
    user_invoke_url = f"{invoke_subdir}0af85661a221.user/"

    # generate a random row number between 0 and 11000
    random_row = random.randint(0, 11000)
    # get the data for the random_row of each table
    pin_data = new_connector.get_records("pinterest_data", random_row)
    geo_data = new_connector.get_records("geolocation_data", random_row)
    user_data = new_connector.get_records("user_data", random_row)

    # pin posting
    pin_payload = json.dumps({
        "records": [
            {"value": pin_data}]
            },
                default=str)               
    pin_response = requests.request("POST", pin_invoke_url, headers=headers, data=pin_payload)
    print(pin_response)

    # geo posting
    geo_payload = json.dumps({
        "records": [
            {"value": geo_data}]
            },
                default=str)               
    geo_response = requests.request("POST", geo_invoke_url, headers=headers, data=geo_payload)
    print(geo_response)

    # user posting
    user_payload = json.dumps({
        "records": [
            {"value": user_data}]
            },
                default=str)               
    user_response = requests.request("POST", user_invoke_url, headers=headers, data=user_payload)
    print(user_response)


if __name__ == "__main__":
    print('Working...')
    start_receiving_post_data_batch()
