import pandas as pd
import psycopg
from sqlalchemy import create_engine
from agents import function_tool
from sqlalchemy import text

# from agents.decorators import tool


#postgresql+psycopg://USERNAME:PASSWORD@HOST:PORT/DATABASE

engine = create_engine(
    "postgresql+psycopg://postgres@localhost:5432/postgres"
)


@function_tool(needs_approval=True)
def delete_orders(order_id: int) -> str:
    """
    Delete an order from the PostgreSQL database using its order_id.
    """
    with engine.begin() as conn:
        result = conn.execute(
            text("DELETE FROM orders WHERE order_id = :order_id"),
            {"order_id": order_id}
        )

    if result.rowcount == 0:
        return f"No order found with order_id {order_id}."

    return f"Order {order_id} deleted successfully."

def run_query(query):
    """
    Execute a SELECT SQL query and return the results.
    """
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df

@function_tool
def execute_query(query:str):
    """
    Execute a SELECT SQL query and return the results.
    """
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df

@function_tool
def list_tables():
    """use this function to get list of tables"""
    query = '''
        select table_name from information_schema.tables
        where table_schema = 'public';
        '''
    table_list = run_query(query)
    return table_list

@function_tool
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
