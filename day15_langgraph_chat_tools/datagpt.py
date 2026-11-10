from dotenv import load_dotenv
from langgraph.graph import StateGraph , START , END
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel
from tools import get_schema,execute_query

from typing import TypedDict , Literal

load_dotenv()

model = ChatAnthropic(model_name='claude-haiku-5-5')

class Query(BaseModel):
    query : str

model_s = model.with_structured_output(Query)

class SQLState(TypedDict):
    question : str
    schema : str
    tables : str
    query : str
    output : str

def get_schema_node(state:SQLState):
    db_schema = get_schema()

    return {'schema' : db_schema}

def get_tables_node(state:SQLState):
    db_schema = state['schema']
    question = state['question']
    prompt = f"""
    Given the user question and full list of tables in the database along with columns. return only the relevent tables and all the columns of those tables.
    question : {question}
    database tables schema : {db_schema}
    """
    response = model.invoke(input=prompt)
    return {'tables': response.text}

def create_sql_node(state : SQLState):
    tables =  state['tables']
    question = state['question']
    prompt = f"""
        create a postgres compatible SQL for the given user question and avaiable tables with their columns names.
        question : {question}
        tables : {tables}
        """
    response = model_s.invoke(input=prompt)
    return {'query' : response.query }

def get_output_node(state:SQLState):
    query = state['query']

    result = execute_query(query)
    return {'output' : result}

graph = StateGraph(SQLState)

graph.add_node('get_schema_node', get_schema_node)
graph.add_node('get_tables_node', get_tables_node)
graph.add_node('create_sql_node', create_sql_node)
graph.add_node('get_output_node', get_output_node)


graph.add_edge(START,'get_schema_node')
graph.add_edge('get_schema_node', 'get_tables_node')
graph.add_edge('get_tables_node', 'create_sql_node')
graph.add_edge('create_sql_node', 'get_output_node')
graph.add_edge('get_output_node', END)


agent = graph.compile()

agent.get_graph().draw_png('graph.png')

initial_state = {'question' : 'give top 5 products by volume'}

final_state = agent.invoke(input=initial_state)

print(final_state['output'])
