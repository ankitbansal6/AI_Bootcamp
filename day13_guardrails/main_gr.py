from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession, handoff, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
import asyncio
from agents.decorators import input_guardrail , output_guardrail

load_dotenv()



@input_guardrail
def input_pii_detection(ctx,agent,input):
    text = str(input)
    if '@' in text:
        is_pii = True
    else:
        is_pii = False
    return GuardrailFunctionOutput(
        output_info= {"pii_detection" : is_pii} ,  
        tripwire_triggered = is_pii,
    )

@output_guardrail
def output_pii_detection(ctx,agent,input):
    text = str(input)
    if '@' in text:
        is_pii = True
    else:
        is_pii = False
    return GuardrailFunctionOutput(
        output_info= {"pii_detection" : is_pii} ,  
        tripwire_triggered = is_pii,
    )


mysession = SQLiteSession("session_1")

agent = Agent(name="orchestrator",
              instructions="you are a helpful customer support agent",
              model="gpt-5.6-luna",
              input_guardrails= [input_pii_detection],
              output_guardrails= [output_pii_detection]
)

async def main():
    try:
        while True:
            user_input = input("ask question: ")
            if user_input=='exit':
                break
            result = await Runner.run(starting_agent=agent,input= user_input, session=mysession)
            print(result.final_output)
    except InputGuardrailTripwireTriggered as exc:
        print("input Guardrail triggered" , exc.guardrail_result.guardrail.name)
    except OutputGuardrailTripwireTriggered as exc:
            print("Output Guardrail triggered" , exc.guardrail_result.guardrail.name)
asyncio.run(main())
