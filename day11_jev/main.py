from typesafe_sdk import TypeSafeClient , Noul,Choice,Score, NoulCriteria
from dotenv import load_dotenv

load_dotenv()


client = TypeSafeClient()

#state = 'I was charged twice. please refund money for 1 transaction. please llok into it immediately'
#state = 'my order has been delayed by 2 days. please cancel and refund my money'
state = {
  "ticket": {
    "subject": "Duplicate charge",
    "messages": [
      {"from": "customer", "text": "I was charged twice for order A-104. Please refund the duplicate."},
      {"from": "support", "text": "We are checking the charges."}
    ]
  },
  "order": {
    "id": "A-104",
    "charges": [
      {"amount_usd": 49, "status": "captured"},
      {"amount_usd": 49, "status": "captured"}
    ]
  },
  "refund_policy": "Duplicate charges are eligible for a refund."
}
criteria = {

    "returns": "Exchanges, wrong or damaged items",
    "shipping": "Delivery status, delays, lost packages",
    "billing": "Charges, invoices, payment problems",
}
criteria_score =[
                    "sev3: not very urgent. can be resolved in 5 days",
                    "sev2: it needs attention . can be resolved in 3 days",
                    "sev1: it needs immediate attention . should be resolved in 24 hours",
                ]

questions = {
    "is_it_urgent" : Noul(instructions="is this customer question needed urgent attention"
                          ,criteria= NoulCriteria(true= "if customer is showing urgency")),
    "ticket_category" : Choice(instructions="which team should handle this"
                        , criteria=criteria),
    "ticket_severity" : Score(instructions="what is the severity level of ticket",
                              criteria=criteria_score)
}

response = client.system_one(state=state,questions=questions)

result = response.answers

#print(result['ticket_severity'])
print(result)
