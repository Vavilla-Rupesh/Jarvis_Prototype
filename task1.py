import requests
import socket
from config import key

def get_ip(host):
    try:
        result = socket.getaddrinfo("google.com",None)
    except Exception as e :
        print(e)
        result = f"Error in find the IP, {e}"
    return result



def temp_room(room):
    result = "Temp = 20, Humidity = 70"
    return result

def temp_city(city):
    url = "https://yahoo-weather5.p.rapidapi.com/weather"

    querystring = {"location":city,"format":"json","u":"f"}

    headers = {
	"X-RapidAPI-Key": "392c833585msh76b3bb13fee211cp175bfajsn228dcfeb154b",
	"X-RapidAPI-Host": "yahoo-weather5.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    d1 = response.json()
    d1 = d1.get("current_observation")
    hum = d1.get("atmosphere").get("humidity")
    temp = d1.get("condition").get("temperature")
    temp = round((temp-32)*5/9,2)
    return (f"Humidity: {hum}, Temp in C: {temp}")



def chat1(chat):
    messages = []  # list which contain all messages
    system_message = f"You are an AI bot, your name is Jarvis find the content related to query : ."  # first instruction
    message = {"role": "user", "parts": [{"text": system_message + " " + chat}]}
    messages.append(message)
    data = {"contents": messages}
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + key
    response = requests.post(url, json=data)
    t1 = response.json()
    # print(t1)
    t2 = t1.get("candidates")[0].get("content").get("parts")[0].get("text")
    print(t2)
    return t2


definitions = [
        {
        "name": "temp_city", #name of the function to be called
        "description": "find the temperature of city",
        "parameters":
            {
            "type":"object",
            "properties":{
                "city":{            # Argument for function temp_city
                    "type":"string",
                    "description":"City to find weather"
                    }
                } 
            }
        },
        {
        "name": "chat1", #name of the function to be called
        "description": "hi hello general message",
        "parameters":
            {
            "type":"object",
            "properties":{
                "chat":{            # Argument for function temp_city
                    "type":"string",
                    "description":"full query asked by user"
                    }
                } 
            }
        },
        {
        "name": "temp_room", #name of the function to be called
        "description": "Find temperature of a my room or my home",
        "parameters":
            {
            "type":"object",
            "properties":{
                "room":{            # Argument for function temp_city
                    "type":"string",
                    "description":"room or home"
                    }
                } 
            }
        },
        
        {
        "name": "get_ip", #name of the function to be called
        "description": "find ip address of given url or domain name",
        "parameters":
            {
            "type":"object",
            "properties":{
                "host":{            # Argument for function temp_city
                    "type":"string",
                    "description":"get url or Domain name"
                    }
                } 
            }
        },
    ]
if __name__=="__main__":
    print(temp_room("room"))