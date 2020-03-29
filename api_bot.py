from flask import Flask, request
from tensorflow.python.keras.backend import set_session
from tensorflow.python.keras.models import load_model
import numpy as np
import flask
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import json
import random


import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

lemmatizer = WordNetLemmatizer()

#tf_config = some_custom_config
sess     = tf.Session()
graph    = tf.get_default_graph()



set_session(sess)
model = load_model('models/chatbot_model.h5')

intents     = json.loads(open('models/intents.json').read())
words       = pickle.load(open('models/words.pkl','rb'))
classes     = pickle.load(open('models/classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for words that exist in sentence
def bag_of_words(sentence, words, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,word in enumerate(words):
            if word == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % word)
    return(np.array(bag))

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

app = Flask(__name__)

# request model prediction
@app.route('/hello', methods=['GET'])
def hello():
    data = {'result': 'Hello!'}
    return flask.jsonify(data)

# request model prediction
@app.route('/predict', methods=['GET'])
def predict():
    
    msg = request.args['msg']

    # Required because of a bug in Keras when using tensorflow graph cross threads
    global sess
    global graph
  
    with graph.as_default():
        set_session(sess)
        
        p   = bag_of_words(msg, words,show_details=False)
        res = model.predict(np.array([p]))[0]

        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        # sorting strength probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
       
        res  = getResponse(return_list, intents)
        data = {'input': msg,'result': res}

        print(data)

        return flask.jsonify(data)

# start Flask server
app.run(host='0.0.0.0', port=5000, debug=False)