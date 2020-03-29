# Chatbot with REST API service

Chatbot, which uses a REST API layer to provide its services, which allows to isolate the chatbot interface from the trainded chatbot  model.


## Install environmet for running and developing
pip install -r requirements.txt

also install the nltk libraries

import nltk
nltk.download('all')

## Creating and traing the chatbot model
1. Add the data for models/intents.json

The format for adding one sample enry :

{

    "tag": "goodbye",

    "patterns": ["Bye, bye","Bye", "See you later", "Goodbye", "Nice chatting to you, bye", "Till next time"],

    "responses": ["Bye, cant wait i see you soon!","See you!", "Have a nice day", "Bye! Come back again soon."],

    "context": [""]
}

This entry must insert to the intents.json file

2. Train the chatbot model
   
   python train_chatbot.py

   After traing the model will be saved into models directory (chatbot_model.h5)

## Start the REST API service

python start api_bot.py will start the RST API service on localhost at port 5000

To configure REST API service change api_bot.py last line
where the Flask server is started.

 * Serving Flask app "api_bot" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

## Start the chatbot

When the REST API service is started the chatbot is ready!

python chatbot.py

you: hey!

bot: Hi there, how can I help?

you: what is the meaning of life?

bot: 42

you: 





