from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

load_dotenv()

def add_tax(price):
    return price * 1.18

runnable = RunnableLambda(add_tax)

#print(runnable.invoke(100))

#user_input = input("tell me about apache spark in 100 words")
#context = []
model = ChatOpenAI(model='gpt-5')
prompt = PromptTemplate(template= """
tell me about {topic} in 100 words
""")

prompt1 = PromptTemplate(template="""
based on below article create 5 quiz questions
{article}
""")
#input = prompt.invoke({'topic': 'spark'})

#result = model.invoke(input=input)

#print(result.text)

# chains 

#runnables 
parser = StrOutputParser()
chain  = prompt | model | parser | prompt1 | model | parser | runnable

# result = chain.invoke({'topic': 'spark'})

# print(result)

#about spark(100) -> llm -> create 10 quiz question based on below content
 
 # langgraph
