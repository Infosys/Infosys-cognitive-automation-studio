'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from win32com.client import Dispatch
from abstract_bot import Bot

class ClassifyReceivedEmailDomainCategory(Bot):
    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:
            domain = executeContext['domain']
            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            inbox = outlook.GetDefaultFolder("6")
            all_inbox = inbox.Items
            folders = inbox.Folders

            if domain == "external":
                sender1 = []
                c=0
                for msg in all_inbox:
                    if msg.Class==43 :
                        if msg.SenderEmailType!='EX':
                            if msg.SenderEmailAddress not in sender1 and msg.SenderEmailAddress.split('@')[-1]!="infosys.com":
                                sender1.append(msg.SenderEmailAddress)
                                c=c+1
                                
                #print(sender1)            
                print('Count of external :',c)

                return {'status':'success'}

            sender = []
            c=0
            for msg in all_inbox:
                if msg.Class==43 and domain == "internal":
                    if msg.SenderEmailType=='EX':
                        if msg.Sender.GetExchangeUser() != None:
                            if msg.Sender.GetExchangeUser().PrimarySmtpAddress not in sender and msg.Sender.GetExchangeUser().PrimarySmtpAddress.split('@')[-1]=="infosys.com":
                                sender.append(msg.Sender.GetExchangeUser().PrimarySmtpAddress)
                                c=c+1
                                
            #print(sender)            
            print('Count of internal :',c) 
            return {'status':'success'}

        except Exception as e: 
            return {'Error occured ': str(e)}

if __name__ == '__main__':
    context = {}
    obj_snow = ClassifyReceivedEmailDomainCategory()
    
    context = {
            'domain' : '',
                } 
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)            

    