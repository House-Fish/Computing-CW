def addSpamMessage(dataType, message):
    print("Adding Data into spam.csv")
        
    data = str(dataType + ',' + message + ",,,")
    
    with open('data/lang_model/spam.csv','r') as spam_file:
        mylist = [line.rstrip('\n') for line in spam_file]
        if data not in mylist:
            with open('data/lang_model/spam.csv','a+') as spam_addon:
                spam_addon.write(str(data+'\n'))
            spam_addon.close()
        spam_file.close()

    print("Data successfully added")

def changeSpamMessage(dataType, message):
    print("Changing Data in spam.csv")
    data = str(dataType + ',' + message + ",,,")
    with open('data/lang_model/spam.csv','r') as spam_file:
        mylist = [line.rstrip('\n') for line in spam_file]
    spam_file.close()

    if data in mylist:
        index = mylist.index(data)
        
        if dataType == "spam":
            dataType = "ham"
        else:
            dataType = "spam"
            
        mylist[index] = str(dataType + ',' + message + ",,,")
    with open('data/lang_model/spam.csv','w') as spam_file:
        for i in range(len(mylist)):
            spam_file.write(mylist[i] + '\n')
    spam_file.close()

    print("Data successfully changed in spam.csv")
