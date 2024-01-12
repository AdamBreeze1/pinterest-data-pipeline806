from database_utils import *


new_connector = AWSDBConnector()

@run_infinitely
def run_infinite_post_data_loop():
    new_connector.connect_and_get_records()

    invoke_url = "https://lly47uv1za.execute-api.us-east-1.amazonaws.com/beta/topics/"
    post_record_to_API("POST", f"{invoke_url}0af85661a221.pin/", new_connector.pin_result)
    post_record_to_API("POST", f"{invoke_url}0af85661a221.geo/", new_connector.geo_result)
    post_record_to_API("POST", f"{invoke_url}0af85661a221.user/", new_connector.user_result)

if __name__ == "__main__":
    print('Working...')
    run_infinite_post_data_loop()
