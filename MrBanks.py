# Copyright (c) 2026 Vihaan Sood. All Rights Reserved.
# Proprietary Source Code - For Demonstration Purposes Only.


from google import genai
import os
from dotenv import load_dotenv
load_dotenv()


client = genai.Client(api_key= os.environ.get("GEMINI_API_KEY"))

sys_instruct = """

You are Mr. Banks, a helpful banking chatbot agent. Your PRIMARY goal is to prevent fraud and your SECONDARY goal is to help the user.

You are alos able to call onto tools when appropriate:

- If the user asks for a calulation, use the 'calculator' tool

"""


#Example tool
def calculator(expression: str):
    """
    Calculates the result of a mathematical expression
    
    :param expression: Description
    :type expression: str
    what
    """

    print("Calculator tool called")
    try:
        return eval(expression)
    except Exception as e:
        return f"Error: {e}"


tools = [calculator]



chat = client.chats.create(
    model="gemini-2.0-flash", 
 
    config=genai.types.GenerateContentConfig(
        tools=tools,
        system_instruction=sys_instruct,
        max_output_tokens=500,
    )
)

while True:
    user_input = input("User Input: ")

    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Mr. Banks: Goodbye.")
        break

    try:
        response = chat.send_message(user_input)
        print(f"Mr. Banks: {response.text}")
        
    except Exception as e:
        print(f"Error: {e}")