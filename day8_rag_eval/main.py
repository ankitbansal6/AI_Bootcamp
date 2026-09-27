from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualRecallMetric, ContextualPrecisionMetric, ContextualRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval import evaluate

query = "What if these shoes don't fit?"
# Replace this with the actual output from your LLM application
actual_output = "We offer a 30-day full refund at no extra cost. We are located in mysore"

# Replace this with the expected output from your RAG generator
expected_output = "You are eligible for a 30 day full refund at no extra cost. Make sure item is not damaged"

# Replace this with the actual retrieved context from your RAG pipeline
retrieval_context = ["item should not be damaged"
                     ,"All customers are eligible for a 30 day full refund at no extra cost."]

metric = AnswerRelevancyMetric(
    threshold=0.7,
    model="gpt-4o",
    include_reason=True
)
test_case = LLMTestCase(
    input= query,
    actual_output=actual_output,
    #expected_output=expected_output,
    #retrieval_context=retrieval_context
)

# To run metric as a standalone
# metric.measure(test_case)
# print(metric.score, metric.reason)

evaluate(test_cases=[test_case], metrics=[metric])
