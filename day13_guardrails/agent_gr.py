from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession, handoff, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
import asyncio
from agents.decorators import input_guardrail , output_guardrail
from guardrails import GuardrailAgent
from pathlib import Path

load_dotenv()


mysession = SQLiteSession("session_1")

agent = GuardrailAgent(name="support agent",
              instructions="you are a helpful customer support agent",
              model="gpt-5.6-luna",
              config=Path("guardrails_config.json")
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
