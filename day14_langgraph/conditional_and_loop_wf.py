from dotenv import load_dotenv
from langgraph.graph import StateGraph , START , END
from langchain_anthropic import ChatAnthropic
from pydantic import BaseModel

from typing import TypedDict , Literal

load_dotenv()

model = ChatAnthropic(model_name='claude-haiku-5-5')

class diet_plan_approval(BaseModel):
    is_approved : Literal[0,1]
    feedback : str

model_structure = model.with_structured_output(diet_plan_approval)

class StateBMI(TypedDict):
    h : float
    w : float
    bmi : float
    label : str
    diet_plan : str
    is_approved : int
    feedback : str
    iteration : int
    max_iteration : int



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
    based on below BMI value of a person , create a daily diet plan. make sure protein is low
    bmi : {bmi}
    """
    reponse = model.invoke(input=prompt)

    return {'diet_plan' : reponse.text}

def diet_plan_route(state: StateBMI):
    bmi = state['bmi']
    if bmi < 20 or bmi > 25 :
        return 'yes'
    else :
        return 'no'

def evaluate_diet_plan(state: StateBMI):
    bmi = state['bmi']
    diet_plan = state['diet_plan']

    prompt = f"""
    based on following criteria and BMI value evalaute the given diet plan.
    criteria : 
    1- There should be enough protien for the diet
    2- There should be enough fibre
    3- calroied should not be very high

    bmi : {bmi}
    diet plan : {diet_plan}

    return 1 if the plan is good else return 0. Also privide feeback.
    """
    reponse = model_structure.invoke(input= prompt)
    return {'is_approved' : reponse.is_approved , 'feedback' :  reponse.feedback}

def optimize_route(state:StateBMI):
    if state['is_approved'] == 1 or state['iteration'] >= state['max_iteration']:
        return 'no'
    else:
        return 'yes'

def optimize_diet(state:StateBMI):
    prompt = f"""
    based on below bmi , original diet plan and feedback, provide the updated optimized diet plan
    bmi : {state['bmi']}
    original diet plan : {state['diet_plan']}
    feedback : {state['feedback']}
    """

    response = model.invoke(input = prompt)

    return {'diet_plan' :  response.text , 'iteration' :  state['iteration'] + 1 }

graph.add_node('bmi' , calculate_bmi)
graph.add_node('labelbmi' , label_bmi)
graph.add_node('diet_plan' , diet_plan)
graph.add_node('evaluate_diet_plan' , evaluate_diet_plan)
graph.add_node('optimize_diet' , optimize_diet)

graph.add_edge(START , 'bmi')
graph.add_edge('bmi', 'labelbmi')
graph.add_conditional_edges('bmi' , diet_plan_route , {'yes' : 'diet_plan', 'no' : END })
graph.add_edge('diet_plan', 'evaluate_diet_plan')
graph.add_conditional_edges('evaluate_diet_plan' , optimize_route , {'yes' : 'optimize_diet', 'no': END })
graph.add_edge('optimize_diet', 'evaluate_diet_plan')
graph.add_edge('labelbmi', END)

agent = graph.compile()

agent.get_graph().draw_png('graph.png')

initial_state = {'h' : 1.8 , 'w' : 90 , 'iteration':1  , 'max_iteration' : 3}

final_state = agent.invoke(input=initial_state)

print(final_state)
