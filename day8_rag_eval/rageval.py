import json 
from retrieval import get_retrieved_docs, get_actual_answer
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from deepeval import evaluate

load_dotenv()

from deepeval.metrics import (
    ContextualRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    FaithfulnessMetric,
    AnswerRelevancyMetric,
)

golden_dataset= []
with open('dataset/golden_dataset.jsonl', 'r') as f:
    for line in f:
        golden_dataset.append(json.loads(line))

def rag(question):

    # Your actual retrieval code
    retrieved_chunks = get_retrieved_docs(question,3)

    # Your actual LLM generation code
    answer = get_actual_answer(
        query=question,
        context=retrieved_chunks
    )

    return answer, retrieved_chunks

#print(golden_dataset[0]['question'])

# print(rag(query))

test_cases = []

for item in golden_dataset:

    question = item["question"]
    expected_answer = item["expected_answer"]

    # Run your RAG
    actual_answer, retrieved_chunks = rag(question)

    test_case = LLMTestCase(
        input=question,
        actual_output=actual_answer,
        expected_output=expected_answer,
        retrieval_context=retrieved_chunks,
    )

    test_cases.append(test_case)

contextual_precision = ContextualPrecisionMetric(
    threshold=0.7,
    include_reason=True,
    model="gpt-4o"
)

contextual_recall = ContextualRecallMetric(
    threshold=0.7,
    include_reason=True,
    model="gpt-4o"
)

faithfulness = FaithfulnessMetric(
    threshold=0.7,
    include_reason=True,
    model="gpt-4o"
)

answer_relevancy = AnswerRelevancyMetric(
    threshold=0.7,
    include_reason=True,
    model="gpt-4o"
)

evaluate(
    test_cases=test_cases,
    metrics=[
        contextual_precision,
        contextual_recall,
        faithfulness,
        answer_relevancy
    ]
    
)
