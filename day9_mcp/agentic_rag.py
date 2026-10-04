from dotenv import load_dotenv
from openai import OpenAI
import json 
from retrieval import ask_question
load_dotenv()

client = OpenAI()


my_tools = [
    {
        "type": "function",
        "name": "ask_question",
        "description": "get context from vector db to answer hr policy related questions",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "user questions"
                }
            },
            "required": ["query"]
        }
    }
]

response = client.responses.create(model='gpt-5',
                        input = "how many sick leaves do i get annually",
                        tools=my_tools)

 #input= 'what is the stock price of Infosys in USD',
response_id = response.id

tool_mapping = {'ask_question': ask_question}
while True:
    tool_outputs = []
    llm_output = response.output
    for item in llm_output:
        if item.type == 'function_call':
            args = json.loads(item.arguments)
            function_name  = item.name
            print(function_name , args)
            call_function = tool_mapping[function_name]
            tool_result = call_function(**args)
            call_id = item.call_id
            tool_outputs.append({"type": "function_call_output",
                            "call_id": call_id,
                                "output": str(tool_result)})

    if not tool_outputs:
        break

    response = client.responses.create(model='gpt-5',
                        input = tool_outputs,
                        previous_response_id = response_id,
                        tools=my_tools)
    response_id = response.id

print(response.output_text)

