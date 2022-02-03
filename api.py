import black
import pandas as pd
import numpy as np
from flask import *
import json, time
import pickle

model_in = open('model_pickle','rb')
pipeline_model = pickle.load(model_in)

updateCount = 0

app = Flask(__name__)

@app.route('/requests/', methods=['GET']) #For official use during actual testing 

# Link: http://127.0.0.1:6969/requests/?phone=97320611&requests=PLACEHOLDER&train=True&dataType=spam

def request_page():

    #get request from api
    phone_number = str(request.args.get('phone'))
    phrase_query = str(request.args.get('requests'))
    train = bool(request.args.get('train'))
    dataType = str(request.args.get('dataType'))
    


    


    d = dict()
    F = open("model/phone_number.csv")
    bl_times =0
    for line in F:
        line = line. strip('\n')
        (key, val) = line. split(",")
        d[key] = val
        if phone_number in d:
            bl_times += 1


    #results from ML of spam
    result = str(pipeline_model.predict(pd.Series(np.array([phrase_query])))[0])
    
    if result == "spam" and bl_times >5:
        result = True
    elif result == "spam":
        result = True
    else:
        result = False


    

    if train == True and (dataType == "spam" or dataType == "ham"):
        
        print("Adding Data into spam.csv")
        
        data = str(dataType + ',' + phrase_query + ","+","+",")
        
        with open('model/spam.csv','r') as spam_file:
            mylist = [line.rstrip('\n') for line in spam_file]
            if data not in mylist:
                with open('model/spam.csv','a+') as spam_addon:
                    spam_addon.write(str(data+'\n'))
                spam_addon.close()
            spam_file.close()
            
        print("Data has been successfully added")


    if train == True and dataType == "spam":
        print("Adding Data into phone_number.csv")
        num_count=1

        d = dict()
        F = open("model/phone_number.csv")
        for line in F:
            line = line. strip('\n')
            (key, val) = line. split(",")
            d[key] = val
        num_count=int((d[phone_number]))+1
        print(num_count)
        num_count=str(num_count)

        data = str(phone_number + ',' + num_count)
        print(data)
        with open('model/phone_number.csv','a+') as number_add:
            number_add.write(str(data+'\n'))
        number_add.close()

        print("Data has been successfully added")
        


    with open('model/spam.csv','r') as spam_count:
        dataPoints = len(list(spam_count))
    spam_count.close()
        
    data_set = {'Count': dataPoints, 'Result': result}
    json_dump = json.dumps(data_set)
    
    return json_dump

if __name__ == '__main__':
    app.run(port=6969)