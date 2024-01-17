import sqlalchemy
import AWSDBConnector_creds as creds
import random

from sqlalchemy import text
from time import sleep


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

        self.random_row = int
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

    def get_records(self, table: str, row_number):
        '''
        Generates a query string from table name and row number arguments and
        executes that query string on a given database connection to obtain a
        row record from a database

        Parameters:
        - table (str): table in database to connect to.
        - row_number (int): selected row record

        Returns:
        - dict: of the selcted row of the table
        '''
        # create database connection
        engine = self.create_db_connector()
        with engine.connect() as connection:
            query_string = text(f"SELECT * FROM {table} LIMIT {row_number}, 1")
            selected_row = connection.execute(query_string)
            for row in selected_row:
                result = dict(row._mapping)
        return result

# Decorator function
def just_keep_running(func):
    '''
    Decorator to run function infinitely at random intervals between 0 and 2
    seconds
    '''
    def inner():
        # generate seed for reproducible 'random' results
        random.seed(100)
        # counts cycles of the function
        post_count = 0
        while True: # can use "while post_count < x:" where x is number of runs
            # pause for a random length of time between 0 and 2 seconds (emulates posts)
            sleep(random.randrange(0, 2))
            func()
            post_count += 1
            if post_count % 10 == 0:
                print(f"{post_count} posts loaded")

    return inner