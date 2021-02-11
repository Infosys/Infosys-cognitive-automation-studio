'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import win32com.client
from datetime import datetime
from abstract_bot import Bot


class FetchUnrespondedEmailsCount(Bot):

   def bot_init(self):  
        pass
        
   def execute(self,executionContext):
        try:
            outlook=win32com.client.Dispatch("Outlook.Application").GetNameSpace("MAPI")
            
            sentItems = []
            sentBox=outlook.GetDefaultFolder(5).Items
            for mailSend in sentBox:
                    mailSentTime = mailSend.SentOn.strftime("%m_%d_%Y")
                    mailSubject =  mailSend.Subject
                    mailString = mailSubject + mailSentTime
                    sentItems.append(mailString)
            
            
            inboxItems = []
            inbox=outlook.GetDefaultFolder(6).Items
            for mailReceived in inbox:
                mailTime = mailReceived.ReceivedTime.strftime("%m_%d_%Y")
                mailSubject =  mailReceived.Subject
                mailString = mailSubject + mailTime
                inboxItems.append(mailString)

            replied = 0
            item=0

            while item < len(inboxItems):
                inboxEmail = inboxItems[item]
                item = item + 1
                for sentItem in sentItems:
                    if inboxEmail == sentItem[4:] or inboxEmail == sentItem:
                        replied = replied + 1
                        
            nonResponded = item - replied
            return{'status':'success', 'notReplied' : nonResponded}
        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == '__main__':
    bot_obj= FetchUnrespondedEmailsCount()
    bot_obj.bot_init()
    context = {}
    output=bot_obj.execute(context)
    print(output)


