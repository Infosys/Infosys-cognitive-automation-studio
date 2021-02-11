'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import win32com.client
from openpyxl.workbook import Workbook
from abstract_bot import Bot

class MergeEmailsToExcel(Bot):

   def bot_init(self):  
        pass
        
   def execute(self,executionContext):
        try:
            filePathForContent=executionContext["filePathForContent"]
            if  not filePathForContent:
                return {'validation error' : 'missing argument filePathForContent'}
            
            outlook=win32com.client.Dispatch("Outlook.Application").GetNameSpace("MAPI")
            inbox=outlook.GetDefaultFolder(6)
            messageBox=inbox.Items
            list=[]
            for message in messageBox:
                list1=[]
                if message.UnRead ==True and message.Class == 43  :
                    msgSub=[message.Subject]
                    msgTo=[message.To]
                    msgBody=[message.Body]
                    msgFrom=[message.SenderName]
                    msgCC=[message.Cc]
                    msgBody1=msgBody[0].replace('\r\n', ' ')
                    list1.append(str(msgTo))
                    list1.append(str(msgFrom))
                    list1.append(str(msgCC))
                    list1.append(str(msgSub))
                    list1.append(str(msgBody1))
                    list.append(list1)
                    
            # Write into excel file 
            headers= ['TO','FROM','Cc','SUBJECT','BODY']# Headers made in Excel file
            workbookName = filePathForContent
            wb = Workbook()
            page = wb.active
            page.title = 'Unread Emails'
            page.append(headers)
            #Appending data
            for info in list:
                page.append(info)
            wb.save(filename = workbookName)
            return{'status':'success'}
        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == '__main__':

    bot_obj= MergeEmailsToExcel()
    context = {
            'filePathForContent':'', 
           
        }
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)


