'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from win32com.client import Dispatch
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot to calculate total number of received emails user replied to.
class CountOfReplyToReceivedEmails(Bot):
    
    def bot_init_(self):
        pass

    def execute(self,executionContext):
        try:               
            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            sent = outlook.GetDefaultFolder(5)
            smessages = sent.Items
            inbox = outlook.GetDefaultFolder(6)
            rmessages = inbox.Items
            reply = []
            for sm in smessages:
                if sm.Subject[0:3]=='Re:' or sm.Subject[0:3]=='RE:' :                         
                    for rm in rmessages:
                        if rm.Subject == sm.Subject[4:] or rm.Subject == sm.Subject:
                            if sm.SentOn > rm.ReceivedTime:
                                if rm.Subject not in reply:
                                    reply.append(rm.Subject)           
                        if rm.Subject[0:3]=='FW:' or rm.Subject[0:4]=='Fwd:':
                            if rm.Subject.split(': ')[-1] == sm.Subject.split(': ')[-1]:
                                if sm.SentOn > rm.ReceivedTime:
                                    if rm.Subject.split not in reply:
                                        reply.append(rm.Subject)  
            outputStatus = 'Total number of received emails user replied to are '+str(len(reply))
            return {'Status': outputStatus}
        except Exception as e:
            return {'Exception': str(e)}
    
if __name__ == "__main__":
    context = {}
    bot_obj = CountOfReplyToReceivedEmails()

    output = bot_obj.execute(context)
    print(output)     