#Boaz - Entire File

def isBlacklistURL(url):
    data = dict()
    num_count = 0
       
    numData = open("data/link_blacklist/links.csv")

    #Organise data in Blacklist into a dictionary
    for line in numData:
        line = line.strip('\n')
        (key, val) = line.split(",")
        data[key] = val
    
    #Check if link is already inside of Blacklist
    try:     
        num_count=int(data[url])
    except:
        pass
    
    return num_count

def addBlacklistURL(url):
    data = dict()

    print("Adding Data into link.csv")
        
    numData = open("data/link_blacklist/links.csv")
    
    #Pull and store data into Dictionary
    for line in numData:
        line = line.strip('\n')
        (key, val) = line.split(",")
        data[key] = val
    numData.close()
    
    #Add data into dictionary 
    if url in data:
        data[url] = str(int(data[url]) + 1)
    else:
        data[url] = 1

    #Write updated data into dictionary
    with open("data/link_blacklist/links.csv", 'w') as file_data:
        for pos in data:
            file_data.write(str(pos) + ',' + str(data[pos])+ '\n')
    
    print("Data successfully written")
    
    return True

def removeBlacklistURL(url):
    data = dict()

    print("Removing Data from links.csv")
        
    numData = open("data/link_blacklist/links.csv")
    
    #Pull and store data into Dictionary
    for line in numData:
        line = line.strip('\n')
        (key, val) = line.split(",")
        data[key] = val
    numData.close()

    #Remove data from dictionary 
    if url in data:
        if int(data[url]) == 1:
            del data[url]
        else:
            data[url] = str(int(data[url]) - 1)
    else:
        return False
    
    #Write updated data into dictionary
    with open("data/link_blacklist/links.csv", 'w') as file_data:
        for pos in data:
            file_data.write(str(pos) + ',' + str(data[pos])+ '\n')
    
    print("Data successfully removed")
    
    return True

def casesURL():
    with open("data/link_blacklist/links.csv", 'r') as data:
        count = len(data.readlines())
    return count

