from guardrails import GuardrailsOpenAI,GuardrailTripwireTriggered
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

client = GuardrailsOpenAI(config=Path("guardrails_config.json"))


try :
    result = client.responses.create(model='gpt-5.6-luna',
                            #instructions="you are a data engineer. please respond to user questions in a precise manner",
                            input = "hi this is ankit. my email is sgsg@gmail.com. tell me my email id")
    print(result.output_text)
except GuardrailTripwireTriggered as exc:
    print("Guardrail Triggered", exc.guardrail_result)

