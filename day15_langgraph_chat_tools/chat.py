from dotenv import load_dotenv
from langgraph.graph import StateGraph , START , END, add_messages 
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel 
from lang_tools import get_schema,execute_query,list_tables
from langchain_core.messages import AIMessage , SystemMessage, HumanMessage, BaseMessage
from langgraph.checkpoint.memory import InMemorySaver


from typing import TypedDict , Literal, Annotated

load_dotenv()

model = ChatAnthropic(model_name='claude-haiku-5-5')

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage] , add_messages] # -> reducer


tools = [execute_query,list_tables,get_schema]

model_with_tools = model.bind_tools(tools=tools)

graph = StateGraph(ChatState)

def chat_node(state:ChatState):
    messages = state['messages']
    response = model_with_tools.invoke(input=messages)
    return {'messages' : [response] }

tools = ToolNode(tools=tools)

graph.add_node('chat_node', chat_node)
graph.add_node('tools', tools)


graph.add_edge(START,'chat_node')
graph.add_conditional_edges('chat_node', tools_condition)
graph.add_edge('tools' , 'chat_node')
graph.add_edge('chat_node' , END)

checkpointer = InMemorySaver()
agent = graph.compile(checkpointer=checkpointer)


# Conversation configuration
config = {"configurable": {"thread_id": "session-1"}}


agent.get_graph().draw_png('graph.png')

while True:
    user_input = input('ask question: ')
    if user_input == 'exit':
        break
    initial_state = {'messages' :[HumanMessage(user_input)] }

    final_state = agent.invoke(input = initial_state, config= config)

    print(final_state['messages'][-1].content)

