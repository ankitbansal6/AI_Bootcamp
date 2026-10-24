import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from agents import function_tool

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

@function_tool
def get_retrieved_docs(query:str , top_k:int):
    """
    args : takes user query and no of documents as input
    returns related documents from the database
    """

    query_embedding = get_embeddings(query)

    related_docs = collection.query(query_embeddings=query_embedding ,n_results = top_k)

    context = related_docs["documents"][0]
    return context

