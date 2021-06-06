# Medical NER

A Spacy NER model trained over messages from patients describing medical conditions.

## Prerequisites

- Python 3.x.
- Docker

## Deployment 

### Deploy with Docker

The model runs thanks to a small Flask app that can be deployed using a Docker container. If you want to use Docker, there's a dockerfile included on this project that you could already use. 

To deploy the docker image, run: 

```bash
docker build -f dockerfile --tag medicalner .
```

After deplying the image, run the app using:

```bash
docker run --name medicalner -p 43656:5000 -t -i medicalner:latest
```

Change the '43656' to the port of your choice.

### Deploying without Docker

To use it without Docker, you will need:

1. Install the packages on the requirements.txt file.
2. Install the "en_core_web_sm" Spacy model. Do it with the command

```bash
$ python -m spacy download en_core_web_sm
```

Due to limiotations regarding the size of the model, you will have toi pull it from an external server. Install the model files using the script in nerflask/utils/getmodel.py.

After this, edit the configs/config.py file and edit the available options. Currently, they are:

1. appdebug: should the app start in debug mode?
2. JSON_SORT_KEYS: When returning the predictions, should JSON keys be sorted?
3. apphost: what's the default host to start the application?

You can run the server as any other Flask app. For more info, visit the [Flask Quickstart](https://flask.palletsprojects.com/en/1.1.x/quickstart/) page.

## Making predictions

Predictions can be made by sending a query to your app instance, using the parameter "t".

An example of quey is:

```python

# import
import requests, json

# text to predict
message = "I’ve had on and off pain in my left testicle for just over two years now. I’ve had a scan to corroborate that I don't have cancer."

# get the url and the params
url     = 'http://127.0.0.1:43656/predict'

# compose the quey
payload = {'t': original_message}
headers = {}

# request a prediction
response = requests.post(url, params=payload, headers=headers)

# return the prediction
prediction = json.loads(response.text)

# see
print(prediction)

```

The response:

```python
{
  "text": "I\u2019ve had on and off pain in my left testicle for just over two years now. I\u2019ve had a scan to corroborate that I don't have cancer.", 
  "predictions": [
    {
      "token": "pain", 
      "start": 20, 
      "end": 24, 
      "entity": "SYMPTOM"
    }, 
    {
      "token": "left", 
      "start": 31, 
      "end": 35, 
      "entity": "POSITION"
    }, 
    {
      "token": "testicle", 
      "start": 36, 
      "end": 44, 
      "entity": "ANATOMY"
    }, 
    {
      "token": "two", 
      "start": 59, 
      "end": 62, 
      "entity": "DATE"
    }, 
    {
      "token": "years", 
      "start": 63, 
      "end": 68, 
      "entity": "DATE"
    }, 
    {
      "token": "scan", 
      "start": 11, 
      "end": 15, 
      "entity": "PROCEDURE"
    }, 
    {
      "token": "don't have", 
      "start": 38, 
      "end": 48, 
      "entity": "NEGATION"
    }, 
    {
      "token": "cancer", 
      "start": 49, 
      "end": 55, 
      "entity": "DISEASE"
    }
  ]
}
```
## Available entities

In addition to Spacy's standard entities, the model is able to recognize: 

1. BRANCH: The specialization, such as "cardiology" or "general practicioner"
2. MEDICALDOCTOR: References to a doctor or to a practicioner. 
3. MENTALHEALTH: References to mental health conditions.
4. DISEASE: References to mental diseases.
5. ANATOMY: References to body parts.
6. DRUG: References to medications.
7. PROCEDURE: References to procedures, such as medical tests.
8. MEDICALTOOL: References to medical tools, such as crutches.
9. POSITION: References to position of the symptom.
10. SYMPTOM: References to symptoms.
11. NEGATION: Explicit negations.
12. JARGON: References to broad medical terms.
13. FAMILY: References to a family member (useful when describing diseases on the family)




















