from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input="show me the tables avaiable in database",
    tools=[
        {
            "type": "mcp",
            "server_label": "datagpt",
            "server_url": "https://staff-viewing-overtone.ngrok-free.dev/mcp",
            #"server_url" : "http://127.0.0.1:8000",
            "require_approval": "never"          
        }
    ]
)

print(response.output_text)
