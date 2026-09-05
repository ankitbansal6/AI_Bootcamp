import pandas as pd
import psycopg
from sqlalchemy import create_engine

#postgresql+psycopg://USERNAME:PASSWORD@HOST:PORT/DATABASE

engine = create_engine(
    "postgresql+psycopg://postgres@localhost:5432/postgres"
)

def execute_query(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df


def get_schema(table_name):
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

# result = execute_query("select * from orders limit 5")
# result = get_schema('orders')
# print(result)
