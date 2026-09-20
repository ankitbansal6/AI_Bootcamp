from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine
import pandas as pd

client = OpenAI()

engine = create_engine(
    "postgresql+psycopg://postgres@localhost:5432/postgres"
)
def execute_query(query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    return df

def get_embeddings(text):
    response = client.embeddings.create(model='text-embedding-3-small',
                            input= text,
                            dimensions=300)
    return response.data[0].embedding

#print(collection.get(ids=['docs/hr_policy.pdf_1']))

user_query = "what is leave policy"

query_embedding = get_embeddings(user_query)

sql_query = f"""
    select content 
    from hr_policy_docs
    order by embedding <=> '{query_embedding}' asc
    limit 5
    """
docs = execute_query(sql_query)
retrieved_docs = docs["content"].tolist()

#print(retrieved_docs)

prompt = f"""
based on the given context answer user question

context : {retrieved_docs}

user_question : {user_query}

Rules:  
1- Give direct and natural answers
2- if you dont have context for question dont make up the answer just say i dont know.
"""

#print(prompt)

response = client.responses.create(model='gpt-5.6-sol',
                                   input=prompt)

print(response.output_text)
