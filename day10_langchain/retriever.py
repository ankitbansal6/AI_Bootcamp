from dotenv import load_dotenv
load_dotenv()

from langchain_chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",dimensions=300
)

vector_store = Chroma(
    collection_name="hr_policy",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

result = vector_store.similarity_search("what is leave policy",k=2 )

print(result)
