'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import traceback
import sys
import win32com.client
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot to read email from outlook
class ReadEmail(Bot):

    def bot_init(self):
        pass

    def execute(self,executionContext):
        application = executionContext['application']

        if application == '':
                return ("Missing argument : application")

        try:
            outlook = win32com.client.Dispatch(application).GetNamespace("MAPI") #Create outlook object
            inbox = outlook.GetDefaultFolder(6)
            mails = inbox.Items
            mail = []
            for m in mails:
                if m.UnRead==True:
                    mail.append(str(m.Body))
            return {'mail_body': mail}
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Error' : formatted_lines[-1]} 

if __name__ == "__main__":
    context = {}
    bot_obj = ReadEmail()
    context = {'application' : ''} #Outlook.Application is input
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
