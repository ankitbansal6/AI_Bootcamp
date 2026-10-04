from bharatstock import BharatStock
import pandas as pd
import psycopg
from sqlalchemy import create_engine
from langchain_core.tools import tool


#postgresql+psycopg://USERNAME:PASSWORD@HOST:PORT/DATABASE

engine = create_engine(
    "postgresql+psycopg://postgres@localhost:5432/postgres"
)

@tool
def execute_query(query):
    '''use this function execute a sql
    args : a query string
    return : query result
    '''
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df

@tool
def list_tables():
    '''this function will list all the tables in database'''
    query = '''
        select table_name from information_schema.tables
        where table_schema = 'public';
        '''
    table_list = execute_query(query)
    return table_list

@tool
def get_schema(table_name):
    ''' this function will provide schema for any given table'''
    query = f'''
            SELECT
    table_name ,       
    column_name,
    data_type
    FROM information_schema.columns
    where table_schema= 'public' and table_name = '{table_name}'
    ORDER BY ordinal_position;
        '''
    schema = execute_query(query)
    return schema
