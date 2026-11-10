import pandas as pd
import psycopg
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://postgres@localhost:5432/postgres"
)


def execute_query(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df.to_string(index=False)


def list_tables():
    query = '''
        select table_name from information_schema.tables
        where table_schema = 'public';
        '''
    table_list = execute_query(query)
    return table_list

def get_schema():
    query = f'''
           SELECT
    table_name ,       
    string_agg(column_name, ',' order by ordinal_position ) as columns
    FROM information_schema.columns
    where table_schema= 'public' 
    group by table_name;
        '''
    schema = execute_query(query)
    return schema

#print(get_schema())
