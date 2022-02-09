import pandas as pd
import re
import pickle

gist_file = open('data/lang_model/gist_stopwords.txt', 'r')

try:
    content = gist_file.read()
    stopwords = content.split(",")
    stopwords = [i.replace('"',"").strip() for i in stopwords]

finally:
    gist_file.close()
    
df = pd.read_csv(r'data/lang_model/spam.csv',encoding='utf-8',on_bad_lines='skip')

# get necessary columns for processing
df = df[['v2', 'v1']]
df = df.rename(columns={'v2': 'messages', 'v1': 'label'})

# check for null values
df.isnull().sum()

STOPWORDS = set(stopwords)

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

    print("Data has been successfully added")

def changeSpamMessage(dataType, message):
    print("Changing Data into spam.csv")
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

    print("Data has been successfully changed")

def clean_text(text):
    # convert to lowercase
    text = text.lower()
    # remove special characters
    text = re.sub(r'[^0-9a-zA-Z]', ' ', text)
    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    # remove stopwords
    text = " ".join(word for word in text.split() if word not in STOPWORDS)
    return text

# clean the messages
df['clean_text'] = df['messages'].apply(clean_text)

X = df['clean_text']
y = df['label']

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

def classify(model, X, y):
    # train test split
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, shuffle=True, stratify=y)
    
    # Training Model
    pipeline_model = Pipeline([('vect', CountVectorizer()),
                              ('tfidf', TfidfTransformer()),
                              ('clf', model)])
    
    pipeline_model.fit(x_train, y_train)
        
    with open('model_pickle','wb') as f:
        pickle.dump(pipeline_model,f)
        
    print('Accuracy:', pipeline_model.score(x_test, y_test)*100)
    y_pred = pipeline_model.predict(x_test) 
    print(classification_report(y_test, y_pred))

from sklearn.svm import SVC
model = SVC(C=3)
classify(model, X, y)

