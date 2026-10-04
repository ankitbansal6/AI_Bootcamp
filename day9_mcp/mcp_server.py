from fastmcp import FastMCP
from bharatstock import BharatStock
import psycopg
from sqlalchemy import create_engine
import pandas as pd
mcp = FastMCP("Demo 🚀")

engine = create_engine(
    "postgresql+psycopg://postgres@localhost:5432/postgres"
)

@mcp.tool
def execute_query1(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df

@mcp.tool
def execute_query(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df

@mcp.tool
def list_tables():
    query = '''
        select table_name from information_schema.tables
        where table_schema = 'public';
        '''
    table_list = execute_query(query)
    return table_list

@mcp.tool
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

@mcp.tool
def get_stock_details(stock_code:str):
    """
    call this function to get stock price details in INR

    args : NSE stock code for a company 

    returns company name and stock price details in INR
    """
    client = BharatStock(api_key="xxx")
    # A single stock, with latest price + derived metrics
    stock = client.stocks.get(stock_code)
    return stock.company_name, stock.latest_price

@mcp.resource("delivery://policy")
def get_delivery_policy() -> str:
    """Get the delivery policy."""
    return """
    Delivery Policy:
    1. Standard delivery takes 3-5 business days.
    2. Express delivery takes 1-2 business days.
    3. Orders can be cancelled before shipment.
    """

@mcp.prompt()
def sql_assistant():
    """Help users write SQL queries."""
    return "You are a SQL expert. Help users write SQL queries."


if __name__ == "__main__":
    #mcp.run()
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000
    )
