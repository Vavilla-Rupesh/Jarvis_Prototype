#this file execute the respective function baesd upon user query
import task1
import requests
from config import key

def parse_function_response(message):
    function_call = message[0].get("functionCall")
    function_name = function_call["name"]   #'temp_city'
    print("Gemini: call function ", function_name)
    try :
        arguments = function_call.get("args","Kolkata")
        print("Gemini: arguments are ", arguments)
        if arguments:
            d = getattr(task1,function_name)
            print("function is ", d)
            function_response = d(**arguments)
        else:
            function_response = "No Arguments are present"
        
    except Exception as e :
        print(e)
        function_response = "Invalid function"
    return function_response

def run_conversation(user_message):
    
    messages = []  # list which contain all messages
    print(user_message)
    system_message = """You are an AI bot that can do everything using function call.
    When you are asked to do something, use the function call you have available
    and then respond with messsage""" # first instruction
    
    message = {"role": "user",
               "parts": [{"text": system_message +"\n"+user_message }]}
    
    messages.append(message)
    
    data = {"contents": [messages], 
            "tools" :
            [ {"functionDeclarations" : task1.definitions
              }]
            }
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + key
    response = requests.post(url, json=data )
    if response.status_code !=200:
        print(response.text)
    
    t1 = response.json()
    # if "content" not in t1.get("candidates"):
    #     print("Error: No content in response")
        
    message = t1.get("candidates")[0].get("content").get("parts")
    print("Message #####:",message)
    if 'functionCall' in message[0]  :
        resp1 = parse_function_response(message)
        print("Actual response", resp1)
        return resp1
    else:
        print("No function call")
    
    # t2 = t1.get("candidates")[0].get("content").get("parts")[0].get("text")
    # print(t2)
    #print("now we are getting ", t1)
    
if __name__=="__main__":
    user_message = "find ip address of google.com"
    print(run_conversation(user_message))
    
"""
now we are getting  {'candidates': [{'content': 
{'parts':
part = [
{'functionCall': {'name': 'temp_city', 'args': {'city': 'Delhi'}}}],
'role': 'model'}, 'finishReason': 'STOP', 'index': 0}], 'promptFeedback': {'safetyRatings': [{'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_HATE_SPEECH', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_HARASSMENT', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'probability': 'NEGLIGIBLE'}]}}
"""