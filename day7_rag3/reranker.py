from sentence_transformers import CrossEncoder
from dotenv import load_dotenv
load_dotenv()


reranker = CrossEncoder(
        "BAAI/bge-reranker-v2-m3"
    )

def rerank_docs(query, docs, top_k):
    pairs = [
        [query, document]
        for document in docs
    ]
    scores = reranker.predict(pairs)
    ranked_documents = sorted(
        zip(docs, scores),
        key=lambda x: x[1],
        reverse=True
    )

    top_documents = [
        document
        for document, score in ranked_documents[:top_k]
    ]
    return top_documents
