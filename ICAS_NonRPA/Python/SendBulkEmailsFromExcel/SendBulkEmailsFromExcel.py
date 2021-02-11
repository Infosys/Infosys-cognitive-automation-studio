'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as p
import win32com.client as win32
from abstract_bot import Bot

class SendBulkEmailsFromExcel(Bot):

   def bot_init(self):  
        pass
        
   def execute(self,executionContext):
        try:
            filePathForEmails =executionContext["filePathForEmails"]
            if  not filePathForEmails:
                return {'validation error' : 'missing argument filePathForEmails'}

            filePathForContent=executionContext["filePathForContent"]
            if  not filePathForContent:
                return {'validation error' : 'missing argument filePathForContent'}

        # To populate content in a string object from a file
            contentString=''
            content=open(filePathForContent,"r")
            for x in content.readlines():
                contentString+=x
            
        # To get all the emails in list from excel file having column name: EmailIDs and sheet name3 as :Sheet1

            emails = p.read_excel(filePathForEmails,sheet_name='Sheet1')
            emailList=emails['EmailIDs'].tolist()

#         Send bulk emails
            outlook = win32.Dispatch('outlook.application')
            for email in emailList:
                mail = outlook.CreateItem(0)
                mail.HTMLBody = contentString
                mail.Subject = 'Test Mail'
                mail.To = email
                mail.send
                print("mail send to : "+ email)

            return{'status':'success'}
        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == '__main__':

    bot_obj= SendBulkEmailsFromExcel()
    context = {
                'filePathForContent':'',
                'filePathForEmails':'',
               
                }
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)


