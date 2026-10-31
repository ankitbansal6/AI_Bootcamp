from dotenv import load_dotenv
from langgraph.graph import StateGraph , START , END
from langchain_anthropic import ChatAnthropic

from typing import TypedDict

load_dotenv()

model = ChatAnthropic(model_name='claude-haiku-5-5')

class StateBMI(TypedDict):
    h : float
    w : float
    bmi : float
    label : str
    diet_plan : str

graph = StateGraph(StateBMI)


def calculate_bmi(state : StateBMI):
    h = state['h']
    w = state['w']

    c_bmi = round(w / (h*h),2)
    return {'bmi' : c_bmi}

def label_bmi(state : StateBMI):
    bmi = state['bmi']
    if bmi < 20:
        c_label = 'low bmi'
    elif bmi < 25 :
        c_label = 'normal bmi'
    else:
        c_label = 'high bmi'
    return {'label' : c_label}

def diet_plan (state: StateBMI):
    bmi = state['bmi']
    prompt = f"""
    based on below BMI value of a person , create a daily diet plan.
    bmi : {bmi}
    """
    reponse = model.invoke(input=prompt)

    return {'diet_plan' : reponse.text}

    

graph.add_node('bmi' , calculate_bmi)
graph.add_node('labelbmi' , label_bmi)
graph.add_node('diet_plan' , diet_plan)

graph.add_edge(START , 'bmi')
graph.add_edge('bmi', 'labelbmi')
graph.add_edge('labelbmi', 'diet_plan')
graph.add_edge('diet_plan', END)

agent = graph.compile()

agent.get_graph().draw_png('graph.png')

initial_state = {'h' : 1.8 , 'w' : 75 }

final_state = agent.invoke(input=initial_state)

print(final_state)
