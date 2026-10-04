from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
from tools import execute_query,get_schema,list_tables


model = ChatOpenAI(model='gpt-5.6-sol')

my_tools = [execute_query,get_schema,list_tables]

model_tools = model.bind_tools(my_tools)

result = model_tools.invoke("give me sql to find top 5 products by volume")

# print(result.content[0]['name'])
# print(result.content[0]['arguments'])

print(result)


