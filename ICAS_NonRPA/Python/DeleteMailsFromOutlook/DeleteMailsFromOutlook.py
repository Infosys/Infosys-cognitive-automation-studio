'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
from win32com.client import Dispatch

# Bot to delete mails of a given subject from outlook
# Input Parameters : Subject, Folder from where email is to be deleted
# (if no folder is given, mail will be deleted from inbox)
# returns success if email is deleted


class DeleteMailsFromOutlook(Bot):

    def bot_init_(self):
        pass

    # execute method for main functionality
    def execute(self, executeContext):
        try:

            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            inbox = outlook.getDefaultFolder("6")
            srcfolderpath = executeContext['srcFolder']
            # if no folder is given, mail will be deleted from inbox
            if srcfolderpath == "":
                srcfolder = inbox
                print("srcFolder is inbox")
            else:
                srcfolder = inbox.Folders(srcfolderpath)
                print("srcFolder is ", srcfolder)

            emails = srcfolder.Items

            # throws exception if no subject is given
            if executeContext['subject'] == "":
                return {'Exception': 'no subject provided'}
            else:
                subject = executeContext['subject']

            # checks each email for the input Subject and deletes email accordingly
            # returns success if email is deleted
            for email in emails:
                print(email, email.Subject)
                if email.Subject == subject:
                    email.Delete()
                    return {'status': 'email deleted'}

        except Exception as e:
            return {'Exception': str(e)}


if __name__ == "__main__":
    output = {}
    #executeContext = {'subject': "RE: my name is aishwarya", 'srcFolder': "MovedTo"}
    executeContext = {'subject':'','srcFolder':''}
    obj = DeleteMailsFromOutlook()
    obj.bot_init_()
    output = obj.execute(executeContext)
    print(output)




