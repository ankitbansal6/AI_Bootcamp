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
def ask_question(query):
    '''
    returns the context for a query to answer hr policy related question
    '''
    #query = "in case of layoff how Severance i will get"
    query_embedding = get_embeddings(query)
    related_docs = collection.query(query_embeddings=query_embedding ,n_results = 5)
    context = related_docs["documents"][0]
    return context

#print(ask_question("what is leave policy"))

