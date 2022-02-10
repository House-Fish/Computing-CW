from data.link_blacklist.url_blacklist import removeBlacklistURL, isBlacklistURL
from data.ph_blacklist.phone_blacklist import isBlacklistPH, removeBlacklistPH
from data.lang_model.model_func import changeSpamMessage

def addProfile(ID,result,message,link,phoneNo):
    dt = dict()
    ID,result,message,link,phoneNo = str(ID), str(result), str(message), str(link), str(phoneNo)

    #id,result,message,link,phoneNo
    print("Adding Data into profile.csv")
    
    sumData = open("data/profile.csv")
    #Pull and store data into Dictionary
    for line in sumData:
        line = line.strip('\n')
        hold = line.split(",")
        dt[hold[0]] = {'result': hold[1],'message':hold[2],'link':hold[3],'phoneNumber': hold[4]}
    
    sumData.close()
    dt[ID] = {'result': result,'message':message,'link':link,'phoneNumber': phoneNo}

    with open("data/profile.csv", 'w') as file_data:
        for pos in dt:
            formatData = str(pos) + ',' + str(dt[pos]['result']) + ',' + str(dt[pos]['message']) + ',' + str(dt[pos]['link']) + ',' + str(dt[pos]['phoneNumber'])
            file_data.write(formatData + '\n')
    
    print("Data successfully written")
    dt.clear()
     
def changeProfile(ID):
    dt = dict()
    ID = str(ID - 1)

    print("Changing Data in profile.csv")
    sumData = open("data/profile.csv")
    #Pull and store data into Dictionary
    for line in sumData:
        line = line.strip('\n')
        hold = line.split(",")
        dt[hold[0]] = {'result': hold[1],'message':hold[2],'link':hold[3],'phoneNumber': hold[4]}
    
    sumData.close()
        
    changeSpamMessage(dt[ID]['result'],dt[ID]['message'])
    
    if dt[ID]['result'] == "spam":
        dt[ID]['result'] = "ham"
    else:
        dt[ID]['result'] = "spam"
        
    if isBlacklistPH(dt[ID]['phoneNumber']) > 0: 
        removeBlacklistPH(dt[ID]['phoneNumber'])
    if isBlacklistURL(dt[ID]['link']) > 0:
        removeBlacklistURL(dt[ID]['link'])
        
    with open("data/profile.csv", 'w') as file_data:
        for pos in dt:
            formatData = str(pos) + ',' + str(dt[pos]['result']) + ',' + str(dt[pos]['message']) + ',' + str(dt[pos]['link']) + ',' + str(dt[pos]['phoneNumber'])
            file_data.write(formatData + '\n')
            
    print("All data successfully changed")
    dt.clear()
    return True

def currentID():
    with open("data/profile.csv", 'r') as data:
        count = len(data.readlines())
    return count

