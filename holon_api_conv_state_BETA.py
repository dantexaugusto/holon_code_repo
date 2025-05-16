#New way to manage Bot's conversation state and context window
#Now using new resources from OpenAI's API
#such as the response.id message identifyer
from openai import OpenAI
from dotenv import load_dotenv
import os
import sqlite3
from datetime import datetime

def llm_transmitter_receiver(input_message, prev_respID):

    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    #Carrega o arquivo de texto com o promt de identidade e comportamento para o modelo
    with open("holon_identity_prompt_00.txt", "r") as promptFile:
        identity_prompt = promptFile.read()
        
    response = client.responses.create(
        model="gpt-4.1-nano",
        previous_response_id=prev_respID,
        instructions=identity_prompt,
        input=input_message,
    )

    responseID_modelAnswer = {
        'response_load': {
            'last_respID': response.id, 
            'text_output': response.output_text
        }
    }
    
    with open("last_respID.txt", "w") as respIdFile:
        respIdFile.write(response.id)
    
                            
    return responseID_modelAnswer

def main():
    #getting and saving messa id from text files 
    #for prototyping purpouses
    try:   
        with open("last_respID.txt", "r") as idFile:
            last_respID = idFile.read()
    except:
        last_respID=None

    user_message = input("User Prompt:")

    model_answer = llm_transmitter_receiver(user_message, last_respID)

    print(f"Holon: {model_answer['response_load']['text_output']}", '\n')

if __name__ == "__main__":
    main()
