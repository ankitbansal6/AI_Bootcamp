from typesafe_sdk import TypeSafeClient , Noul,Choice,Score, NoulCriteria
from dotenv import load_dotenv

load_dotenv()


client = TypeSafeClient()

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
	"Employees absent for more than 5 consecutive days without informing the company may face termination proceedings.",
    "i love my company"
]

state = {
    "query" : "what is sick leave policy",
    "documents" : {
        'd1' : "Employees can carry forward a maximum of 6 unused annual leave days to the next calendar year.",
        'd2' : "Employees can take up to 6 days of sick leave for medical reasons.."
    }  
    }

questions = {
"is_d1_relevent" : Noul(instructions= "will the  document d1  help in answering user query"),
"is_d2_relevent" : Noul(instructions= "will the  document d2  help in answering user query")
}

response = client.system_one(state=state,questions=questions)

result = response.answers

print(result)








# for document in documents:
#     state = {
#     "query" : "what is leave policy",
#     "document" : document  
#     }

#     questions = {
#     "is_it_relevent" : Noul(instructions= "will the given document help in answering user query")
#     }

#     response = client.system_one(state=state,questions=questions)

#     result = response.answers

#     print(document,result['is_it_relevent'].noul)
