def isBlacklistPH(phoneNum):
    data = dict()
    num_count = 0
    
    numData = open("data/ph_blacklist/phone-number.csv")

    #Organise data in Blacklist into a dictionary
    for line in numData:
        line = line.strip('\n')
        (key, val) = line.split(",")
        data[key] = val
    
    #Check if number is already inside of Blacklist
    try:     
        num_count=int(data[phoneNum])
    except:
        pass
    
    return num_count

def addBlacklistPH(phoneNum):
    data = dict()
    phoneNum = str(phoneNum)

    print("Adding Data into phone-number.csv")
    
    numData = open("data/ph_blacklist/phone-number.csv")
    
    #Pull and store data into Dictionary
    for line in numData:
        line = line.strip('\n')
        (key, val) = line.split(",")
        data[key] = val
    numData.close()
    
    #Add data into dictionary 
    if phoneNum in data:
        data[phoneNum] = str(int(data[phoneNum]) + 1)
    else:
        data[phoneNum] = 1

    #Write updated data into dictionary
    with open("data/ph_blacklist/phone-number.csv", 'w') as file_data:
        for pos in data:
            file_data.write(str(pos) + ',' + str(data[pos])+ '\n')
    
    print("Data successfully written")
    
    return True

def removeBlacklistPH(phoneNum):
    data = dict()
    phoneNum = str(phoneNum)

    print("Changing Data in phone-number.csv")

    numData = open("data/ph_blacklist/phone-number.csv")
    
    #Pull and store data into Dictionary
    for line in numData:
        line = line.strip('\n')
        (key, val) = line.split(",")
        data[key] = val
    numData.close()

    #Remove data from dictionary 
    if phoneNum in data:
        if int(data[phoneNum]) == 1:
            del data[phoneNum]
        else:
            data[phoneNum] = str(int(data[phoneNum]) - 1)
    else:
        return False
    
    #Write updated data into dictionary
    with open("data/ph_blacklist/phone-number.csv", 'w') as file_data:
        for pos in data:
            file_data.write(str(pos) + ',' + str(data[pos])+ '\n')
    
    print("Data successfully changed in phone-number.csv")
    
    return True

def casesPH():
    with open("data/ph_blacklist/phone-number.csv", 'r') as data:
        count = len(data.readlines())
    return count

