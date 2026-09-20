from chunking import create_chunks
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import text
import psycopg
from sqlalchemy import create_engine

#postgresql+psycopg://USERNAME:PASSWORD@HOST:PORT/DATABASE

engine = create_engine(
    "postgresql+psycopg://postgres@localhost:5432/postgres"
)

client = OpenAI()

def get_embeddings_batch(texts):
    response = client.embeddings.create(model='text-embedding-3-small',
                            input= texts,
                            dimensions=300)
    embeds = []
    for item in response.data:
        embedding = item.embedding
        embeds.append(embedding)
    return embeds

chunks, ids, metadatas = create_chunks('docs/hr_policy.pdf',500,100)
embeddings = get_embeddings_batch(chunks)

def add_data(chunks, embeddings):
    for chunk, embedding in zip(chunks, embeddings):
        query = text("""
            INSERT INTO hr_policy_docs
                (content, embedding)
            VALUES
                (:content, :embedding)
        """)
    
        with engine.begin() as conn:
            conn.execute(
                query,
                {
                    "content": chunk,
                    "embedding": str(embedding)
                }
            )

add_data(chunks, embeddings)
