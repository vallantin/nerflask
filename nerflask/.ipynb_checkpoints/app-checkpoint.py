# flask
from flask import Flask, jsonify, request

# load model
import spacy

# normalize
from textacy import preprocessing 

# variables
from utils.configs.config import appdebug, JSON_SORT_KEYS, apphost

# logs
import logging

# start app
app = Flask(__name__)

# turn mode debug on or off
app.debug = appdebug

# don't sort keys
app.config['JSON_SORT_KEYS'] = JSON_SORT_KEYS

#---------------------------------------------------------------------------------------
#------------------------------------- Endpoints ---------------------------------------
#---------------------------------------------------------------------------------------

@app.route('/predict', methods=['GET','POST'])
def predict():

    """ **predict()**
    
        Interface to return the named entities on a text.
     
        Args:
            
        **t** (str): The text to detect the entities
   
    """
    # get the argument text
    text = request.args.get('t')

    # get the entities after prediction
    entities = predict_logic(text = text, nlp = nlp)

    # transform the entities into a dictionary
    predictions = {'text' : text, 'predictions': entities}

    # return
    return jsonify(predictions)


#---------------------------------------------------------------------------------------
#-------------------------------------- Logic ------------------------------------------
#---------------------------------------------------------------------------------------

def predict_logic(text:str, nlp):

    """ **predict_logic()**
    
        Returns the named entities on a text.
     
        Args:
            
        **text** (str): The text to detect the entities
        **nlp**       : The spacy object to detect the entities
   
    """
    # normalize text
    text = normalize(text)

    # convert the text to spacy doc
    doc = nlp(text)

    # get the entities
    entities = [{"token":ent.text, "start": ent.start_char-ent.sent.start_char, "end": ent.end_char-ent.sent.start_char, "entity": ent.label_} for ent in doc.ents]

    # return 
    return entities

def normalize(text:str) -> str:

    """ **normalize(text:str) -> str** 
    
        Process a string using a pipeline. Will put all normalization steps into a normalization pipeline.
    
        **Args:**
            
        **text** (str): The text to normalize. 
            
    """
    text = text.lower()
    text = preprocessing.normalize.unicode(text)
    text = preprocessing.replace.user_handles(text, 'USER')
    text = preprocessing.replace.phone_numbers(text, 'PHONE')
    text = preprocessing.replace.emails(text, 'EMAIL')
    text = preprocessing.replace.urls(text, 'URL')
    text = text.strip()
    
    return text

#---------------------------------------------------------------------------------------
#------------------------------------- Execute -----------------------------------------
#---------------------------------------------------------------------------------------

if __name__ == '__main__':

    # start the logging config
    logging.basicConfig(filename='logs/logs.log',
                         filemode='a',
                         format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                         level=logging.DEBUG)

    logging.info('Server started')

    # start prediction pipe for reviews
    nlp = spacy.load(f"model/") #load the best model

    # Add the sentecizer
    nlp.add_pipe('sentencizer')

    # run the app
    app.run(host=apphost)