# Spammed 

**Spammed** is an API that idenifies possibly harmful and dangerous messages! This is done through through an assesment of the **language used in the message**, a **blacklist of websites found in the message** & a **list of blacklisted phone numbers**. This program can be used directly by software developers with Messaging apps or even by freelance developers hoping to create an app to indentify these Messages in widely used apps. (E.g.Whatsapp, IMessage or Facebook Messanger) 

# Installation
This document has been updated for the latest version of this project.

## Step 1: Git installation
Apple ships a binary package of Git with Xcode. However, to ensure that you have the most updated version, you can run this piece of code in your terminal.

``` Bash
$ git clone https://github.com/git/git
```

Should this return an error, head to https://git-scm.com/download/mac to download Git

## Step 2: Clone Project
The next step of installing our project requires you to have Git installed. If you have not done so, please go back to Step 1. If it has already been installed, the next thing you will need to do is to **clone the repository**. This step will also take place in your terminal, we recommend that you clone this repository in a directory that you will easily be able to access. This can be done by using the `cd` command in terminal,
``` Bash
$ cd directoryName
```
After having moved to the directory of your choice, use this command to clone this repository, 
``` Bash
$ git clone https://github.com/JappyJY/Computing-CW.git
```
It will take a few seconds to clone the entire repository, depending on the speed of your internet. If the repository has been successfully cloned, it should not return any errors. If you do face any errors, we recommend that you head to https://docs.github.com/en/repositories/creating-and-managing-repositories/troubleshooting-cloning-errors to find out how to resolve them.

## Step 3: Locate and Activate Environment
Now that you have successfully cloned our project, you will need to locate the cloned project and activate the environment. This can be done by using the `cd` command again. However, this time we will need to go to this specific directory, `Computing-CW`. Ensure that your terminal is still in the directory that you have cloned the project and run this command, 
``` Bash
$ cd Computing-CW/
```
If no errors have occured, you should be in the directory `Computing-CW`. If you are facing any errors, please read through Step 2 and 3 again. Now that you have located the directory, you will need to activate the **python virtual environment**. It has been saved directly in the repository for your ease of use. However, if you do not have it installed, you will need to run this command, 
``` Bash
$ python3 -m pip install --user virtualenv
```
If the command does not return any errors, you can go ahead with the following code to activate the environment, 
``` Bash
$ source env/bin/activate
```
If this command does not return any errors, the words (env) should appear on the left most side of the terminal. If so, you have successfully installed and activated this environment. 

## Step 4: Running code
Now that you have successfully installed and activated all the neccessary programs, you can go ahead with using the program. We have split the program into two main files, `main.py` and `api.py` which are both found in the parent directory of the cloned repository. If you would like to run the API, you will need to run the command, 
``` Bash
$ python3 api.py
```
This could take a few seconds to load or possibly even stall as this is the first time it is being ran, you can use `Ctrl + C` in the terminal and run it again. After having ran the program, it will open up a Flask Development server on the port 6969 on your network. To access the API, you will have to type the follow in any web browser, replacing the placeholders with the respective information.
``` HTML
http://127.0.0.1:6969/requests/?phone=PLACEHOLDERFORPHONENUMBER&requests=PLACEHOLDERFORMESSAGE
```
The API will return a JSON format response which is commonly used in API's, if you would like to see it better, you can go over to https://jsonformatter.curiousconcept.com/, pasting the API response in the text box. If you would like to test the program without using the API, you can run it using `main.py`, running the following command in your terminal,  
``` Bash
$ python3 main.py
```
Following the instructions as shown in the terminal. 

# Examples
Examples of code that you can use to test the program, 
## main.py
Example #1:
* 91237712, Hi, my name is Jay Liew and i would like to welcome you to School of Science of Technology, end
* Train Model: N

_Ham, Your message is  safe_

Example #2:

* 97320611, You are awarded a SiPix Digital Camera! call 09061221061 from landline. Delivery within 28days. T Cs Box177. M221BP. 2yr warranty., end
* Train Model: N

_Spam, Your message is not safe_

Example #3:

* 97320605, PRIVATE! Your 2003 Account Statement for shows 800 un-redeemed S.I.M. points. Call 08718738001 Identifier Code: 49557 Expires 26/11/04, at 3?, end
* Train Model: N

_Spam, Your message is not safe_

Example #4:

* 92972803, Hi, I would like to contact you about your cya tryouts, could i find you tomorrow after school, at 3?, end
* Train Model: N

_Ham, Your message is  safe_

## api.py
Example #1: 
* http://127.0.0.1:6969/requests/?phone=97320611&requests=omg%20how%20was%20your%20trip%20to%20japan?%20i%20heard%20you%20had%20alot%20of%20fun%20there.

{
   "id":4,
   "message":"omg how was your trip to japan?? i heard you had alot of fun there.",
   "result":"ham",
   "response":[
      {
         "type":"langModel",
         "langRes":false,
         "testCaseModel":5591
      },
      {
         "type":"phBlack",
         "PHRes":true,
         "testCasePH":11
      },
      {
         "type":"linkBlack",
         "URLRes":false,
         "testCaseURL":72
      }
   ]
}

Example #2: 
* http://127.0.0.1:6969/requests/?phone=97320611&requests=ASKED%203MOBILE%20IF%200870%20CHATLINES%20INCLU%20IN%20FREE%20MINS.%20INDIA%20CUST%20SERVs%20SED%20YES.%20L8ER%20GOT%20MEGA%20BILL.%203%20DONT%20GIV%20A%20SHIT.

{ "id": 5, "message": "ASKED 3MOBILE IF 0870 CHATLINES INCLU IN FREE MINS. INDIA CUST SERVs SED YES. L8ER GOT MEGA BILL. 3 DONT GIV A SHIT.", "result": "spam", "response": [ { "type": "langModel", "langRes": true, "testCaseModel": 5592 }, { "type": "phBlack", "PHRes": true, "testCasePH": 11 }, { "type": "linkBlack", "URLRes": false, "testCaseURL": 73 } ] }

Example #3:
* http://127.0.0.1:6969/requests/?phone=97320611&requests=PRIVATE!%20Your%202003%20Account%20Statement%20for%20shows%20800%20un-redeemed%20S.I.M.%20points.%20Call%2008718738001%20Identifier%20Code:%2049557%20Expires%2026/11/04,%20at%203?

{ "id": 6, "message": "PRIVATE! Your 2003 Account Statement for shows 800 un-redeemed S.I.M. points. Call 08718738001 Identifier Code: 49557 Expires 26/11/04, at 3?", "result": "spam", "response": [ { "type": "langModel", "langRes": true, "testCaseModel": 5593 }, { "type": "phBlack", "PHRes": true, "testCasePH": 11 }, { "type": "linkBlack", "URLRes": false, "testCaseURL": 74 } ] }