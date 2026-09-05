# we want to make a api request to openai
from openai import OpenAI
from dotenv import load_dotenv
#import os
from mydb import execute_query , get_schema

load_dotenv()

#my_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()


schema = get_schema('orders')

while True:
    user_input  = input("Ask your question: ") # give me top 5 states by sales
    if user_input == 'exit':
        break

    final_prompt = f''' generate a postgres SQL based on below schema
    {schema}
    question : {user_input}

    Just give SQL only. wherever possible use left join
    '''
    # print(final_prompt)

    response = client.responses.create(model='gpt-5.6-sol',
                            input= final_prompt)

    query = response.output_text

    result = execute_query(query)

    print(query)
    print(result)

