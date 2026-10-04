from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",dimensions=300
)

# read a file (pypdf) -> chunking (length based ,  recursive chunking) -> embedding -> chromdb
# doclument_loader (langchain-pymupdf4llm) -> (text splitters) -> openaiembedding -> langchain_chromdb

# document  = (page_content , metadata) 

loader = PyMuPDF4LLMLoader("docs/hr_policy.pdf",mode='single')

docs = loader.load()


headers_to_split_on = [
    ("#", "heading_1"),
   # ("##", "heading_2"),
   # ("###", "heading_3"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)


chunks = splitter.split_text(docs[0].page_content)

from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="hr_policy",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",  # Where to save data locally, remove if not necessary
)

vector_store.add_documents(chunks)
