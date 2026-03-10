from langchain_ollama import ChatOllama

def user_validation_node(account_id: str, last_four_digits: str, date_of_birth: str)->bool:
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
       
    llm = ChatOllama(
        model="sqlcoder", 
        temperature=0, # temp = 0 because we want most accurate response possible 
    )

    schema = """
    Table ACCOUNTS:
    - account_id (INT)
    - customer_name (TEXT)
    - date_of_birth (TEXT)
    """

    prompt = f"### Tasks: {account_id, last_four_digits,date_of_birth}\n\n### Schema:\n{schema}\n\n### Response: SELECT"

    response = llm.invoke(prompt)
    return "SELECT" + response.content

if __name__ == "__main__":

    # Test
    print("--- Starting Validation Node ---")
    
    # Raw input string
    user_input = "my name is Jack Jones, ID is 2848902 and DOB is 12/1/1999"
    
    # Manually passing data for testing
    id_val = "2848902"
    last_4 = "8902"
    dob = "12/1/1999"

    # Capture the result
    result = user_validation_node(id_val, last_4, dob)
    
    # Print the result so you can see it in the terminal
    print(f"Validation Result: {result}")
    print("--- Task Finished ---")

