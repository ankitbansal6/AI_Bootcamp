from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel,Field


class Output(BaseModel):
    is_urgent : str = Field(description="return 1 if customer shows urgency")

load_dotenv()

client = OpenAI()

context = """
based on below message from a user tell if it is uregnt

message: I was charged twice. please refund money for 1 transaction. please look into it immediately
"""

response = client.responses.parse(model='gpt-5.6-luna',
                        input = context,
                         text_format= Output )

result = response.output_parsed

print(result.is_urgent)
