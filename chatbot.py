import requests
import datetime

url = "http://localhost:5000/predict"

# Makes a function that will contain the
# desired program.
def dialouge_loop():

    # Calls for an infinite loop that keeps executing
    # until leaving intention is detected occurs
    while True:
        
        you_input = str(input("you: "))
        
        if you_input != "bye":
                        
            payload = {'msg':you_input}
            resp = requests.get(url,params=payload)

            if resp.status_code != 200:
                # This means something went wrong.
                raise('GET /response/ {}'.format(resp.status_code))
            else:
                json_response = resp.json()
                print("bot: " + json_response['result'])      
                
        else:
            print("Bye bye")
            break

# The function is called
dialouge_loop()
