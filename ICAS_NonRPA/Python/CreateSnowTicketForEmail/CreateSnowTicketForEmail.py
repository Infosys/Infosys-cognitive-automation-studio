'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

from abstract_bot import Bot
from ast import literal_eval
import pysnow

import re

from rake_nltk import Rake
from nltk.corpus import stopwords 

class CreateSnowTicketForEmail(Bot):
    def bot_init(self):
        pass
        
    def execute(self, executeContext):
        try:
            instanceID=executeContext['instanceID']
            userName=executeContext['userName']
            passWord=executeContext['passWord']
            emailData=executeContext['emailData']
        
            if not instanceID:
                return{'Missing Argument':'instanceID'}
            if not userName:
                return{'Missing Argument':'userName'}
            if not passWord:
                return{'Missing Argument':'passWord'}
            if not emailData:
                return{'Missing Argument':'emailData'}
            
            emailData1=literal_eval(emailData)
            description=''
            shortDescription=''
            r=Rake()
            result=''
            
            for i in emailData1:

                subject=i['Subject'].lower()
                print(subject)
                if 'ticket' in  subject or 'snow' in subject:
                    if 'snow' in i['Body'].lower():
                        descriptionSearch = re.findall(r"'(.*?)'", i['Body'])   # fetching last single-quotes enclosed value i.e description from email body
                        if descriptionSearch:
                            description = descriptionSearch[-1]
                        a=r.extract_keywords_from_text(description)
                        b=r.get_ranked_phrases_with_scores()
                        shortDesc=[]
                        for key in b:
                            shortDesc.append(key[1])
                        shortDescription=shortDesc[0:3] #fetching top 3 keywords from description provided for short description of the ticket
                        
                        if description and shortDescription:
                            try:
                                c = pysnow.Client(instance=instanceID, user=userName, password=passWord) #establishing connection with SNOW server
                                incident = c.resource(api_path='/table/incident')

                                # Set the payload
                                newTicket = {'short_description': shortDescription,'description': description}
                                # Create a new incident record
                                result = incident.create(payload=newTicket)
                                respList=(str(result._response.content))
                                if "failure" in respList:
                                    result="failure"
                                    print(result)
                                else:
                                    result="Ticket Created"
                                    print(result)

                            except Exception as e:
                                result="Exception: "+str(e)
                                print(result)
                                
                        else:
                            print('Info : Description for the ticket not found')
                    else:
                        print('Info : "SNOW" keyword not found in the email body')
                else:
                    print('Info : Email subject is without keywords "SNOW" or "Ticket"')
            print ("=========================================")
            print ("All emails processed")
            if result=="Ticket Created":
                return {'status': 'Successful'}
            elif result=="failure":
                return{'status':'Failure Occured '+respList}
            elif 'Exception' in result:
                return{'Exception':result}
            else:
                return{'status':'Unable to create ticket'}
        except Exception as e:
            return {'Exception': str(e)}

       
        
if __name__ == '__main__':
    context = {}
    bot_obj = CreateSnowTicketForEmail()

    context = {
                'instanceID': '',
                'userName': '',
                'passWord': '',
                'emailData' : ''
                 #'instanceID': 'dev82133',
                 #'userName': 'admin',
                 #'passWord': 'password',
                 #'emailData' : '[{"Sender": "User1", "Subject": "Create ticket in SNOW", "Body": "Hello,create ticket in SNOW with description \'DELETE THIS ! TESTING ONLY\'."}, {"Sender": "User 2", "Subject": "Create Email", "Body": "Hello,create ticket in SNOW with description \'DELETE THIS ! TESTING ONLY\'."}]'
                
              
            }
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print('output : ',output)
                            
            