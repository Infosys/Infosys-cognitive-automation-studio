'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
from win32com.client import Dispatch
 
class MoveChainemailsToOutlookFolder(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:
            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            inbox = outlook.GetDefaultFolder("6")
            allInbox = inbox.Items
            subject = executeContext['subject']
            
            folder = executeContext['folder']

            if subject is None:
                return {"Missing argument : subject"}
            if folder is None:
                return {"Missing argument : folder"}

            doneBox = outlook.GetDefaultFolder(6).Folders(folder) 
            for msg in allInbox:
                if (msg.Subject == subject):
                    msg.Move(doneBox)
            return {'output': 'Mail moved'}
        except Exception as e: 
            return {'Error occured ': str(e)}

        
if __name__ == '__main__':
    context = {}
    obj_snow = MoveChainemailsToOutlookFolder()
    context = {
            'subject' : '',
            'folder' : '',
                }
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
   