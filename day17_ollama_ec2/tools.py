import pandas as pd
import psycopg
from sqlalchemy import create_engine
from langchain.tools import tool

engine = create_engine(
    "postgresql+psycopg://postgres:postgres123@localhost:5432/postgres"
)



def run_query(query):
    """
    Execute a SELECT SQL query and return the results.
    """
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df

@tool
def execute_query(query:str):
    """
    Execute a SELECT SQL query and return the results.
    """
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df

@tool
def list_tables():
    """use this function to get list of tables"""
    query = '''
        select table_name from information_schema.tables
        where table_schema = 'public';
        '''
    table_list = run_query(query)
    return table_list

@tool
def get_schema(table_name:str):
    """this function take a table name as input and returns its schema"""

    query = f'''
            SELECT
    table_name ,       
    column_name,
    data_type
    FROM information_schema.columns
    where table_schema= 'public' and table_name = '{table_name}'
    ORDER BY ordinal_position;
        '''
    schema = run_query(query)
    return schema
