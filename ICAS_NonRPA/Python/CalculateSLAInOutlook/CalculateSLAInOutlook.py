'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import win32com.client
from openpyxl.workbook import Workbook
from datetime import datetime
from abstract_bot import Bot


class CalculateSLAInOutlook(Bot):

   def bot_init(self):  
        pass
        
   def execute(self,executionContext):
        try:
            filePathForOutput=executionContext["filePathForOutput"]
            if  not filePathForOutput:
                return {'validation error' : 'missing argument filePathForOutput'}
            outlook=win32com.client.Dispatch("Outlook.Application").GetNameSpace("MAPI")
            SentItems=outlook.GetDefaultFolder(5)
            SentBox=SentItems.Items
            list=[]
            list2=[]
            for mailSend in SentBox:
                if mailSend.Subject[0:3]=="Re:" or mailSend.Subject[0:3]=="re:" or mailSend.Subject[0:3]=="RE:" :
                    Inbox=outlook.GetDefaultFolder(6)
                    inbox=Inbox.Items
                    for mailReceived in inbox:
                        if mailReceived.Subject == mailSend.Subject[4:]:
                            list1=[]
                            msgSub=mailReceived.Subject
                            msgRecieveDate=mailReceived.ReceivedTime
                            recieveDate=msgRecieveDate.strftime("%m/%d/%Y %H:%M:%S")
                            msgRespondedTime=mailSend.SentOn
                            respondedTime=msgRespondedTime.strftime("%m/%d/%Y %H:%M:%S")
                            receive=datetime.strptime(recieveDate, '%m/%d/%Y %H:%M:%S')
                            respond=datetime.strptime(respondedTime, '%m/%d/%Y %H:%M:%S')
                            list1.append(msgSub)
                            list1.append(recieveDate)
                            list1.append(respondedTime)
                            timeDifference=respond-receive
                            days, seconds = timeDifference.days, timeDifference.seconds
                            hours = days * 24 + seconds // 3600
                            minutes = (seconds % 3600) // 60
                            seconds = seconds % 60
                            diff=str(hours)+" hours" +str( minutes )+" minutes" + str(seconds) +" seconds"
                            list1.append(diff)
                            if str(mailReceived.Subject) not in list2:
                                list2.append(mailReceived.Subject)
                                list.append(list1)
            
            
# Write into excel file 
            headers= ['SUBJECT','RECEIVE DATE&TIME','RESPOND DATE&TIME',' Calculated SLA']# Headers made in Excel file
            workbookName = filePathForOutput
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
    bot_obj= CalculateSLAInOutlook()
    
    context = {
        'filePathForOutput':''
        }
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)


