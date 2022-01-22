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

# Link: http://127.0.0.1:6969/requests/?requests=PLACEHOLDER&train=True&dataType=spam

def request_page():
    phrase_query = str(request.args.get('requests'))
    train = str(request.args.get('train', default=None, type=None))
    dataType = str(request.args.get('type', default=None, type=None))
    
    result = str(pipeline_model.predict(pd.Series(np.array([phrase_query])))[0])
    
    if result == "spam":
        result = True
    else:
        result = False

    if train == True and dataType != None:
        
        data = str(dataType + ',' + phrase_query + ","+","+",")
        
        with open('model/spam.csv','r') as spam_file:
            mylist = [line.rstrip('\n') for line in spam_file]
            if data not in mylist:
                with open('model/spam.csv','a+') as spam_addon:
                    spam_addon.write(str(data+'\n'))
                spam_addon.close()
            spam_file.close()

    with open('model/spam.csv','r') as spam_count:
        dataPoints = len(list(spam_count))
    spam_count.close()
        
    data_set = {'Count': dataPoints, 'Result': result}
    json_dump = json.dumps(data_set)
    
    return json_dump

if __name__ == '__main__':
    app.run(port=6969)