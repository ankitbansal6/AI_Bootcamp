from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEndpoint , ChatHuggingFace
from dotenv import load_dotenv
from pydantic import BaseModel,Field

load_dotenv()

class SQLOutput(BaseModel):
    sql : str
    explanation : str = Field(description='this should have explanation of the answer generated')

model = ChatOpenAI(model='gpt-5.6-sol')
model_structured = model.with_structured_output(SQLOutput)

result = model_structured.invoke("give me sql to get top 5 products by sales from orders table")

print(result.sql)
print(result.explanation)



#model = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

# llm = HuggingFaceEndpoint (
#     repo_id = "meta-llama/Llama-3.3-70B-Instruct",
#     task = "text-generation"
# )

# model = ChatHuggingFace(llm=llm)

# conversation = []
# conversation.append(SystemMessage("you are a senior data engineer. Answer the user question in 3-4 points"))

# while True:
#     query = input("ask question: ")
#     conversation.append(HumanMessage(query))
#     result = model.invoke(input=conversation)
#     conversation.append(AIMessage(result.content))
#     print(result.text)



