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