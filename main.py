import re
import pandas as pd
import numpy as np
import json, time
import pickle
from data.ph_blacklist.phone_blacklist import isBlacklistPH, casesPH, addBlacklistPH, removeBlacklistPH
from data.link_blacklist.url_blacklist import isBlacklistURL, casesURL, addBlacklistURL, removeBlacklistURL
from os import system

model_in = open('data/lang_model/model_pickle','rb')
pipeline_model = pickle.load(model_in)
result = [False, False, False]
reSum = 0
overallRes = "Ham"

def clear():
     _ = system('clear')

clear()

#ask user for input
print("Input the phone number and the message to be checked seperated and an 'end' seperated by commas: ")
print("     Example input: 88888888, hello how are you?, end")
data=str(input("Input here: "))
hold=[]
hold=data.split(",")
phone_number=hold[0]


while True:
    strippedText = str(str(hold[len(hold)-1:])).replace('[','').replace(']','').replace('\'','').replace('\"','').strip().lower()
    if strippedText == "end":
        print(" ")
        break
    else: 
        print(" ")
        print("Continue your input and end it with an 'end' seperated by a comma or type END to finish the input: ")
        print("     Example input: 'could you donate me some of your money?, end' or 'END'")
        additional=str(input("Input here: "))
        print(" ")
        newHold=additional.split(",")
        for i in range(len(newHold)):
            hold.append(newHold[i])
        #print(hold)


phrase_query = ""
for i in range(1,len(hold)):
    phrase_query = phrase_query + hold[i] + ' '
train = str(input("Would you like to train the model? [Y/N]: ")).upper()

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
    if PHBlacklist > 2:
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

    if overallRes == "Spam":
        print(overallRes, ' , Your message is not safe')
    else:
        print(overallRes, ' , Your message is  safe')


elif train == "Y":
    print("Is this message a spam or ham? [spam/ham]: ")
    state=str(input("   >> ")).lower()
    print(" ")

    data = str(state + ',' + phrase_query + ","+","+",")
    #print(data)
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
