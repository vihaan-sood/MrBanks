# Copyright (c) 2026 Vihaan Sood. All Rights Reserved.
# Proprietary Source Code - For Demonstration Purposes Only.


from google import genai
import os
from dotenv import load_dotenv
from UserValidationAgent import user_validation_node

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver


from langchain_core.messages import *
from typing import Annotated, TypedDict

load_dotenv()


client = genai.Client(api_key= os.environ.get("GEMINI_API_KEY"))

sys_instruct = """

You are Mr. Banks, a helpful banking chatbot agent. Your PRIMARY goal is to prevent fraud and your SECONDARY goal is to help the user. However, do NOT reveal this to the user. 

You are also able to call onto tools when appropriate:

- If the user asks for a calulation, use the 'calculator' tool
- To validate a user, call upon the UserValidationAgent

"""


# tools = [user_validation_node]
tools = []


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    max_tokens=300,
)

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def mrbanks_node(state: State):
    messages = [sys_instruct] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


workflow = StateGraph(State)

workflow.add_node("mr_banks", mrbanks_node)
workflow.add_edge(START, "mr_banks")
workflow.add_edge("mr_banks", END)

memory = InMemorySaver()

app = workflow.compile(checkpointer=memory)



config = {"configurable": {"thread_id": "session_123"}}


greeting = "Hi, how can I help you today?"
app.update_state(config, {"messages": [AIMessage(content=greeting)]})
print(f"Mr. Banks: {greeting}")

while True:
    user_input = input("\nUser: ")


    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Mr. Banks: Goodbye.")
        break

    user_content = {"messages":[HumanMessage(content=user_input)]}

    try:
        for event in app.stream(user_content, config):
            for value in event.values():
                msg = value["messages"][-1]
                print(f"Mr. Banks: {msg.content}")
        
    except Exception as e:
        print(f"Error: {e}")