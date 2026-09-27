import chromadb
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

def get_embeddings(text):
    response = client.embeddings.create(model='text-embedding-3-small',
                            input= text,
                            dimensions=300)
    return response.data[0].embedding

db_client = chromadb.PersistentClient("./chroma_db")

collection = db_client.get_or_create_collection(name="hr_docs")


#print(collection.get(ids=['docs/hr_policy.pdf_1']))


def get_retrieved_docs(query , top_k):

    query_embedding = get_embeddings(query)

    related_docs = collection.query(query_embeddings=query_embedding ,n_results = top_k)

    context = related_docs["documents"][0]
    return context


def get_actual_answer(query,context):

    prompt = f"""
    based on the given context answer user question

    context : {context}

    user_question : {query}

    Rules:  
    1- Give direct and natural answers
    2- if you dont have context for question dont make up the answer just say i dont know.
    """

    #print(prompt)

    response = client.responses.create(model='gpt-5.6-sol',
                                    input=prompt)

    return response.output_text
