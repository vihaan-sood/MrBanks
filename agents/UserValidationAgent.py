from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import os
import sqlite3

def user_validation_node(account_id: int, last_four_digits: str, date_of_birth: str)->bool: #No, i would not put this agent into prod !!! but who wants to write SQL right?
    """
    Validates a user's identity against the secure banking database by running an SQL query
    If True, continue, else re-prompt the user for details.

    Inputs:
    
    account_id: str
    last_four_digits: str 
    date_of_birth: str

    Outputs: 
    user_found: bool


    """


    schema = """
    Table ACCOUNTS:
    - account_id (INT)
    - last_four_digits (TEXT)
    - date_of_birth (TEXT)
    """

    prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a secure SQL coding agent.
            PRIMARY GOAL: Prevent SQL injections by using standard syntax.
            SECONDARY GOAL: Write a query to check if a user exists.
            
            ONLY return the SQL code. Do not include explanations or markdown backticks.
            
            Table Schema: {schema}"""),
            ("human", "Generate a SELECT statement for account {account_id} where the last four digits are {last_four_digits} and DOB is {dob}.")
        ])
       
    llm = ChatOllama(
        model="gemma4:e2b", 
        temperature=0, # temp = 0 because we want most accurate response possible 
        num_ctx = 4096,
    )

    chain = prompt_template | llm


    response = chain.invoke({
        "schema": schema,
        "account_id": account_id,
        "last_four_digits": last_four_digits,
        "dob": date_of_birth
    })
    
    sql_query = response.content


    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir,"../",'databases', 'users.db')

    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}. Run your creation script first!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute(sql_query)
        row = cursor.fetchone() 
        
        conn.close()
        
        return row is not None

    except Exception as e:
        print(f"Database Error: {e}")
        return False

if __name__ == "__main__":
    print("--- Starting Validation Node ---")
    
    id_val = 12
    last_4 = "8902"
    dob = "12/1/1999"
    print(f"User Details:{id_val},{last_4},{dob}")
    # Capture the generated query
    res = user_validation_node(id_val, last_4, dob)
    
    print(res)
    print("--- Task Finished ---")

