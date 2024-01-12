from database_utils import *


new_connector = AWSDBConnector()

@run_infinitely
def run_infinite_post_data_loop():
    '''
    Utilises decorator to run infinitely at random intervals, calls class method
    to get records and then prints those records to the console.
    '''
    new_connector.connect_and_get_records()
    # row_index = new_connector.random_row
    print(f"\n\rRow index number: {new_connector.random_row}\n\r")
    print(new_connector.pin_result)
    print("-"*100)
    print(new_connector.geo_result)
    print("-"*100)
    print(new_connector.user_result)
    print("-"*100)
    # print(type(row_index))

if __name__ == "__main__":
    print('Working...')
    run_infinite_post_data_loop()