import chromadb
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from chunking import create_chunks
import os

client = OpenAI()

def get_embeddings(text):
    response = client.embeddings.create(model='text-embedding-3-small',
                            input= text,
                            dimensions=300)
    return response.data[0].embedding

def get_embeddings_batch(texts):
    response = client.embeddings.create(model='text-embedding-3-small',
                            input= texts,
                            dimensions=300)
    embeds = []
    for item in response.data:
        embedding = item.embedding
        embeds.append(embedding)
    return embeds
    

db_client = chromadb.PersistentClient("./chroma_db")

collection = db_client.get_or_create_collection(name="hr_docs", configuration={ "hnsw": {"space": "cosine"}})

#os.listdir('docs')

#doc_path = 'docs/hr_policy.pdf'
folder = 'docs'
files = os.listdir('docs')

for file in files:
    doc_path = f'{folder}/{file}'
    chunks, ids, metadatas  = create_chunks(doc_path,chunk_size=500,overlap_size=100)
    embeddings = get_embeddings_batch(chunks)
    collection.add(ids=ids,documents=chunks,embeddings=embeddings,metadatas=metadatas)

