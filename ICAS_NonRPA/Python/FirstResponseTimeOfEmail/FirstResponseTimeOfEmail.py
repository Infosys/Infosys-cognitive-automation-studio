'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from files.abstract_bot import Bot
from win32com.client import Dispatch

class FirstResponseTimeOfEmail(Bot):

    def bot_init_(self):
        pass

    def execute(self, executeContext):
        try:
            emailSubject = executeContext['emailSubject']
            #print(emailSubject,type(emailSubject))
            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            inbox = outlook.GetDefaultFolder(6)
            inboxMsgs = inbox.Items
            receivedTime = ""
            sentTime = ""
            
            for mail in inboxMsgs:
                if mail.subject == emailSubject:
                    #print("inside if loop",mail.subject)
                    receivedTime = mail.ReceivedTime
                    
            sentItems = outlook.GetDefaultFolder(5)
            sentMsgs = sentItems.Items
            sentMsgs.Sort("[SentOn]", True)
            for mail in sentMsgs:
                if mail.subject == "RE: "+emailSubject:
                    #print("inside if loop",mail.subject)
                    sentTime = mail.SentOn
            
            #print(receivedTime)
            #print(type(sentTime),sentTime)
            diff = sentTime - receivedTime
            minutes = divmod(diff.seconds, 60)
            
            #respTime = minutes[0].str()+'minutes'+minutes[1].str()+'seconds'
            #print("First Response Time is {} minutes".format(minutes[0]))
            return {'Status':'Success','FirstResponseTime': str(minutes[0])+" minutes"}
        except Exception as e:
            return {'Exception': str(e)}


if __name__ == '__main__':
    
    context = {}
    bot_obj = FirstResponseTimeOfEmail()
    context = {'emailSubject':''}
#    context = {'emailSubject':'Code for review'}
    output = bot_obj.execute(context)
    print(output)
