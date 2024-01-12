import requests
import random
import json
import sqlalchemy
import AWSDBConnector_creds as creds

from time import sleep
from sqlalchemy import text


# generate seed for reproducible 'random' results
random.seed(100)

class AWSDBConnector:
    '''
    This class contains methods for establishing a connection to a database 
    using SQLAlchemy and acquiring records from the connected database
    '''
    def __init__(self):
        self.HOST = creds.HOST
        self.USER = creds.USER
        self.PASSWORD = creds.PASSWORD
        self.DATABASE = creds.DATABASE
        self.PORT = creds.PORT

        # self.random_row = int
        self.pin_result = {}
        self.geo_result = {}
        self.user_result = {}
        
    def create_db_connector(self):
        '''
        Uses sqlalchemy.create_engine() method to generate connection engine
        using credentials contained in AWSDBConnector_creds. Returns engine object.
        '''
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


    def get_record_from_table(self, table: str, connection, row_number: int):
        '''
        Generates a query string from table name and row number arguments and
        executes that query string on a given database connection to obtain a
        row record from a database

        Parameters:
        - table (str): table in database to connect to.
        - connection (engine): database engine connection
        - row_number (int): selected row record

        Returns:
        - dict: of the selcted row of the table
        '''
        query_string = text(f"SELECT * FROM {table} LIMIT {row_number}, 1")
        selected_row = connection.execute(query_string)
        for row in selected_row:
            result = dict(row._mapping)
        return result
    
    def connect_and_get_records(self):
        '''
        Generates a random integer for selecting a random row from the database,
        creates a database connection, and then obtains said row record from each
        of the three tables in the database
        '''
        # generate a random row number between 0 and 11000
        self.random_row = random.randint(0, 11000)
        # create database connection
        engine = self.create_db_connector()

        with engine.connect() as connection:
            # get row record for random row from three separate tables
            self.pin_result = self.get_record_from_table("pinterest_data", connection, self.random_row)
            self.geo_result = self.get_record_from_table("geolocation_data", connection, self.random_row)
            self.user_result = self.get_record_from_table("user_data", connection, self.random_row)



def post_record_to_API(method, invoke_url, selected_rows):
    '''
    Parameters:
    - method (string): like PUT, or POST
    
    '''
    for row in selected_rows:
        result = dict(row._mapping)
        payload = json.dumps({
            "records": [
                {"value": result}]
                },
                    default=str)
        
        headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
        response = requests.request(method, invoke_url, headers=headers, data=payload)
        
        print(response)


# if __name__ == "__main__":
#     # First start the API Rest proxy
#     new_post = PostToAWS()
#     new_post.run_infinite_post_data_loop()
#     print('Working')

def run_infinitely(func):
    '''
    Decorator to run function infinitely at random intervals between 0 and 2
    seconds
    '''
    def inner():
        post_count = 0
        while True:
            # pause for a random length of time between 0 and 2 seconds (emulates posts)
            sleep(random.randrange(0, 2))
            func()
            post_count += 1
            if post_count % 10 == 0:
                print(f"{post_count} posts loaded")

    return inner