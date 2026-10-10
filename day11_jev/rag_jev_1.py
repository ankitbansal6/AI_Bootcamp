
from dotenv import load_dotenv
from typesafe_sdk import TypeSafeClient, Choice, Noul, Score


load_dotenv()

client = TypeSafeClient()

query = "What is the sick leave policy?"

documents = [
    "Employee need to login for 8 hours",
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


# Shared state: every question sees the same query and documents
state = {
    "query": query,
    "documents": {
        f"C{i+1}": document
        for i, document in enumerate(documents)
    }
}

# One relevance decision per candidate document
questions = {
    f"C{i+1}": Noul(
        instructions=(
            f"Does document C{i+1} help answer the user's query? "
         )
    )
    for i in range(len(documents))
}
#print(questions)
response = client.system_one(
    state=state,
    questions=questions
)

# Inspect the probabilities for each document
for i in range(len(documents)):
    key = f"C{i+1}"
    answer = response.answers[key]

    print(f"{key}: {answer.noul}")
    #print(answer.probabilities)
