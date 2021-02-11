'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from win32com.client import Dispatch
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot to calculate total number of sent emails user received a reply for.
class CountOfReceivedReplyEmails(Bot):
    
    def bot_init_(self):
        pass

    def execute(self,executionContext):
        try:               
            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            sent = outlook.GetDefaultFolder(5)
            smessages = sent.Items
            inbox = outlook.GetDefaultFolder(6)
            rmessages = inbox.Items 
            receivedReply = []
            for rm in rmessages:
                if rm.Subject[0:3]=="Re:" or rm.Subject[0:3]=="RE:" :                         
                    for sm in smessages:
                        if sm.Subject == rm.Subject[4:] or rm.Subject == sm.Subject:
                            if rm.ReceivedTime > sm.SentOn:
                                if sm.Subject not in receivedReply:
                                    receivedReply.append(sm.Subject)
                        if sm.Subject[0:3]=='FW:' or sm.Subject[0:4]=='Fwd:':
                            if sm.Subject.split(': ')[-1] == rm.Subject.split(': ')[-1]:
                                if rm.ReceivedTime > sm.SentOn:
                                    if sm.Subject not in receivedReply:
                                        receivedReply.append(sm.Subject)  
            outputStatus = 'Total number of sent emails user received a reply for are '+str(len(receivedReply)) 
            return {'Status': outputStatus}
        except Exception as e:
            return {'Exception': str(e)}
    
if __name__ == "__main__":
    context = {}
    bot_obj = CountOfReceivedReplyEmails()

    output = bot_obj.execute(context)
    print(output)     