#Jia Yu - Entire File

import re
import pandas as pd
import numpy as np
from flask import *
import json
import pickle
from data.lang_model.model_func import addSpamMessage
from data.ph_blacklist.phone_blacklist import addBlacklistPH, isBlacklistPH, casesPH
from data.link_blacklist.url_blacklist import addBlacklistURL, isBlacklistURL, casesURL
from data.profiler import currentID, addProfile, changeProfile

model_in = open('data/lang_model/model_pickle','rb')
pipeline_model = pickle.load(model_in)

app = Flask(__name__)

# Link: http://127.0.0.1:6969/requests/?phone=97320611&requests=PLACEHOLDER

@app.route('/requests/', methods=['GET']) #For official use during actual testing 

def request_page():

    result = [False, False, False]
    phrase_list = []
    
    reSum = 0
    overallRes = "ham"
    
    #get request from api
    phone_number = str(request.args.get('phone'))
    phrase_query = str(request.args.get('requests'))
        
    #remove ',' from phrase_query
    phrase_list = phrase_query.split(',')
    
    phrase_querydata = " "
    for i in range(len(phrase_list)):
        phrase_querydata = phrase_query + phrase_list[i]
    
    #Boaz contributed to this portion of the Regex code
    #blackList links
    try:
        url = re.findall(r'(https?:\/\/)?(\w+(\.\w+)+)(\/\w*)*', phrase_querydata)[0][1]
        URLBlacklist = isBlacklistURL(url)
        link = url

    except:
        URLBlacklist = -1
        link = None

    #blackList phone numbers 
    PHBlacklist = isBlacklistPH(phone_number)

    #langResult from ML of spam
    langRes = str(pipeline_model.predict(pd.Series(np.array([phrase_query])))[0])
        
    if langRes == "spam":
        result[0] = True
    if PHBlacklist > 2:
        result[1] = True
    if URLBlacklist > 2:
        result[2] = True
    
    for i in range(3):
        if result[i] == True:
            reSum += 1
            
    if reSum >= 2:
        overallRes = "spam"
        addBlacklistPH(phone_number)
        if URLBlacklist != -1:
            addBlacklistURL(url)
        
    addSpamMessage(overallRes,phrase_query)
    addProfile(currentID(),overallRes,phrase_query,link,phone_number)
    
    with open('data/lang_model/spam.csv','r') as data:
        casesModel = len(data.readlines())

    data_set = {"id": currentID(), "message": phrase_query, "result": overallRes,"response": [{"type": "langModel","langRes": result[0],"testCaseModel": casesModel},{"type": "phBlack","PHRes": result[1],"testCasePH": casesPH()},{"type": "linkBlack","URLRes": result[2],"testCaseURL": casesURL()}]}
    
    json_dump = json.dumps(data_set, indent = 4)
    
    return json_dump

@app.route('/return/', methods=['GET']) #For official use during actual testing 

def error_page():
    
    #get request from api
    ID = int(request.args.get('id'))
        
    if changeProfile(ID) == True:
        json_dump = json.dumps("Successfully changed result")
    else:
        json_dump = json.dumps("Failed to change result")
    
    return json_dump
    
if __name__ == '__main__':
    app.run(port=6969)
    