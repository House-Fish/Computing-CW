import re
import pandas as pd
import numpy as np
from flask import *
import json, time
import pickle
from data.ph_blacklist.phone_blacklist import isBlacklistPH, casesPH
from data.link_blacklist.url_blacklist import isBlacklistURL, casesURL

model_in = open('data/lang_model/model_pickle','rb')
pipeline_model = pickle.load(model_in)

app = Flask(__name__)

@app.route('/requests/', methods=['GET']) #For official use during actual testing 

# Link: http://127.0.0.1:6969/requests/?phone=97320611&requests=PLACEHOLDER&train=True&dataType=spam

def request_page():

    result = [False, False, False]
    reSum = 0
    overallRes = "Ham"
    
    #get request from api
    phone_number = str(request.args.get('phone'))
    phrase_query = str(request.args.get('requests'))
    train = bool(request.args.get('train'))
    dataType = str(request.args.get('dataType'))
    
    #blackList URL
    try:
        url = re.findall(r'(https?:\/\/)?(\w+(\.\w+)+)(\/\w*)*', phrase_query)[0][1]
        URLBlacklist = isBlacklistURL(url)

    except:
        URLBlacklist = 0

    #blackList phone numbers 
    PHBlacklist = isBlacklistPH(phone_number)

    #langResult from ML of spam
    msgFormat = pd.Series(np.array([phrase_query]))
    langRes = str(pipeline_model.predict(msgFormat)[0])
    
    if langRes == "spam":
        result[0] = True
    if PHBlacklist > 5:
        result[1] = True
    if URLBlacklist > 2:
        result[2] = True
    
    for i in range(3):
        if result[i] == True:
            reSum += 1
            
    if reSum >= 2:
        overallRes = "Spam"
    
    with open('data/lang_model/spam.csv','r') as data:
        casesModel = len(data.readlines())
    
    data_set = "PLACEHOLDER"
    json_dump = json.dumps(data_set)
    
    return json_dump

if __name__ == '__main__':
    app.run(port=6969)
    
'''
    data_set = {
        "id": 1,
        "message": phrase_query,
        "result": overallRes,
        "response": [
            {
                "type": "langModel",
                "langRes": result[0],
                #"accuracy": INT,
                "testCase": casesModel
            },
            {
                "type": "phBlack",
                "langRes": result[1],
                "testCase": casesPH
            },
            {
                "type": "linkBlack",
                "langRes": result[2],
                "testCase": casesURL
            }
        ],
        "error": {
            "ERROR OOPSIE"
        }    
    }
'''