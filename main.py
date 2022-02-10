import re
import pandas as pd
import numpy as np
import json, time
import pickle
from data.ph_blacklist.phone_blacklist import isBlacklistPH, casesPH, addBlacklistPH, removeBlacklistPH
from data.link_blacklist.url_blacklist import isBlacklistURL, casesURL, addBlacklistURL, removeBlacklistURL

model_in = open('data/lang_model/model_pickle','rb')
pipeline_model = pickle.load(model_in)
result = [False, False, False]
reSum = 0
overallRes = "Ham"



#ask user for input

data=str(input("input the phone number and the message to be checked seperated by a comma: "))
phone_number, phrase_query=data.split(",")
train = str(input("Would you like to train the model? [Y/N]: "))

if train == "N":
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

    #data_set = "PLACEHOLDER"
    print(overallRes)


elif train == "Y":
    print("test point 2")
    state=str(input("is this a spam or ham? [spam/ham]: "))

    data = str(state + ',' + phrase_query + ","+","+",")
    print(data)
    with open('data/lang_model/spam.csv','r') as spam_file:
        mylist = [line.rstrip('\n') for line in spam_file]
        if data not in mylist:
            with open('data/lang_model/spam.csv','a') as spam_addon:
                spam_addon.write(str(data+'\n'))
            spam_addon.close()
    spam_file.close()

    if state == "spam":
        addBlacklistPH(phone_number)

        try:
            url = re.findall(r'(https?:\/\/)?(\w+(\.\w+)+)(\/\w*)*', phrase_query)[0][1]
            addBlacklistURL(url)
        except:
            pass


    print("Training complete")


'''
import pandas as pd
import numpy as np
import pickle 

model_in = open('model_pickle','rb')
pipeline_model = pickle.load(model_in)

inputdata = input("Input the message: ")
result = pipeline_model.predict(pd.Series(np.array([inputdata])))

if result == ['ham']:
    print("Your SMS is clean")
    case = "ham"
else:
    print("Your SMS is possibly a SCAM!")
    case = "spam"

checkIf = input("Is the response expected? [y/n]")

while True:
    try:
        if checkIf == "y" or checkIf == "n":
            pass
    except Exception:
        checkIf = input("Is the response expected? [y/n]")
        continue
    break

if checkIf == "y":
    pass
elif result == ['ham']:
    case = "spam"
else:
    case = "ham"

data = str(case + ',' + inputdata + ","+","+",")

with open('spam.csv','r') as spam_file:
    mylist = [line.rstrip('\n') for line in spam_file]
    if data not in mylist:
        with open('spam.csv','a') as spam_addon:
            spam_addon.write(str(data+'\n'))
        spam_addon.close()
spam_file.close()
'''