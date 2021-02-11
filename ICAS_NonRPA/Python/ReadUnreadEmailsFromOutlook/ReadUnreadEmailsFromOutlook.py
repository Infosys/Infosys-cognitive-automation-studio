'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import json
import win32com.client
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot to read unread emails from outlook
class ReadUnreadEmailsFromOutlook(Bot):

    def bot_init(self):
        pass

    def execute(self,executionContext):
        try:
            outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace("MAPI") #Create outlook object
            inbox = outlook.GetDefaultFolder(6)
            mails = inbox.Items
            mail = []
            for m in mails:
                if m.UnRead==True:
                    mail.append({"Sender":(str(m.SenderName)),
                                "Subject":(str(m.Subject)),
                                "Body":(str(m.Body))
                                })                  
            return {'MailList': json.dumps(mail)}  
        except Exception as e:
            return {'Exception': str(e)}
             

if __name__ == "__main__":
    context = {}
    bot_obj = ReadUnreadEmailsFromOutlook()
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)