from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession, handoff
from agents.extensions.memory import AdvancedSQLiteSession
from tools import execute_query,list_tables,get_schema, delete_orders
from retrieval import get_retrieved_docs
import asyncio

load_dotenv()

mysession = SQLiteSession("session_1")
#mysession = AdvancedSQLiteSession(session_id="session_3", db_path="conversations.db", create_tables=True) 


sql_agent = Agent(name="SQL Agent",
              model="gpt-5.6-luna",
              instructions="You are a sql agent. Use tools if required to answer user questions",
              tools= [get_schema,execute_query,list_tables,delete_orders]
              )

hr_agent = Agent(name="HR Agent",
              model="gpt-5.6-luna",
              instructions="You are a helpful hr agent. Use tools if required to answer user questions",
              tools= [get_retrieved_docs]
              )

# agent = Agent(name="orchestrator",
#               instructions="you are a orchestrator agent. use this sub agents to answer user query",
#               model="gpt-5.6-luna",
#               tools= [sql_agent.as_tool(tool_name="sql_agent",tool_description="use this agent to answer quesries using postgres db using sql")
#               , hr_agent.as_tool(tool_name="hr_agent",tool_description="use this agent to answer HR policy related questions")
#               ]
# )

agent = Agent(name="orchestrator",
              instructions="you are a orchestrator agent. use this sub agents to answer user query",
              model="gpt-5.6-luna",
              handoffs= [sql_agent,hr_agent]
)

async def main():
    while True:
        user_input = input("ask question: ")
        if user_input=='exit':
            break
        result = await Runner.run(starting_agent=agent,input= user_input, session=mysession)
        while result.interruptions:
            state = result.to_state()
            for interruption in result.interruptions:
                print("approval for: ", interruption.name)
                print("args : ", interruption.arguments)
                approval = input("approved? Y/N: ")
                if approval == 'Y':
                    state.approve(interruption)
                else:
                    state.reject(interruption)
                result = await Runner.run(starting_agent=agent,input= state, session=mysession)
        print(result.final_output)

asyncio.run(main())
