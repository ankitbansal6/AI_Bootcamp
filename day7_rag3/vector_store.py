from langchain_core.vectorstores import InMemoryVectorStore
from dotenv import load_dotenv
from langchain_openai.embeddings import OpenAIEmbeddings
from reranker import rerank_docs
from keyword_search import get_keywords_docs

load_dotenv()

documents = [
    "Employees can carry forward a maximum of 6 unused annual leave days to the next calendar year.",
    "Employees receive 18 days of annual leave every year.",
    "Employees can take up to 6 days of sick leave for medical reasons.",
    "Unused sick leave cannot be carry forwarded to the next year.",
    "Employees may carry forward unused compensatory off days, subject to manager approval.",
    "Annual leave requests must be submitted at least one week in advance.",
    "Employees can accumulate up to 30 days of annual leave over multiple years.",
    "Unused annual leave exceeding the carry-forward limit will expire at the end of the year.",
    "Employees receive 12 days of sick leave every year.",
    "Public holidays are separate from annual leave and do not count toward the annual leave balance.",
    "Employees can carry forward up to 3 unused causal leave days.",
    "Managers must approve all leave requests through the leave management system.",
    "Employees get 10 casual leaves every year",
    "Employees are entitled to a 1-hour lunch break from 1:00 PM to 2:00 PM during normal working days.",
	"Employees absent for more than 5 consecutive days without informing the company may face termination proceedings."
]

embedding  = OpenAIEmbeddings(model='text-embedding-3-small')

vector_store = InMemoryVectorStore(embedding)

vector_store.add_texts(texts=documents)

query = "how many leaves i can carry forward to next year?"

results = vector_store.similarity_search(
    query,
    k=5
)

retreived_docs =[]
for doc in results:
    retreived_docs.append(doc.page_content)


keyword_docs = get_keywords_docs(documents,query,5)

combined_docs = list(set(retreived_docs + keyword_docs))

#reranked_top3 = rerank_docs(query,retreived_docs,3)
reranked_top3 = rerank_docs(query,combined_docs,3)

print(reranked_top3)

# latency -> send question -> response 
