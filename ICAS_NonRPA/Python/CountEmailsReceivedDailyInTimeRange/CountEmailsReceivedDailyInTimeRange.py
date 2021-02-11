'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import win32com.client
from pandas import pandas, DataFrame
from datetime import datetime, timedelta, date
from abstract_bot import Bot


#the bot is to get the count of mails received daily for a specified period
class CountEmailsReceivedDailyInTimeRange(Bot):

    def bot_init(self):
        pass

    def execute(self, executionContext):
        try:
            startDate=executionContext['startDate']
            endDate=executionContext['endDate']
            startTime=executionContext['startTime']
            endTime=executionContext['endTime']
            excelPath=executionContext['excelPath']

            if startDate=='':
                return {'Exception': 'Missing argument startDate'}
            if endDate=='':
                return {'Exception': 'Missing argument endDate'}
            if startTime=='':
                return {'Exception': 'Missing argument startTime'}
            if endTime=='':
                return {'Exception': 'Missing argument endTime'}
            if excelPath=='':
                return {'Exception': 'Missing argument excelPath'}

            dateFormat='%Y-%m-%d'
            timeFormat='%H:%M'

            if startDate.lower()=='today':
                startDate=datetime.now().date()
            else:
                try:
                    startDate=datetime.strptime(startDate, dateFormat).date()
                except Exception:
                    return {'Exception': 'Incorrect format for startDate. It should be "YYYY-MM-DD" or "today"'}

            if endDate.lower()=='today':
                endDate=datetime.now().date()
                endDate+=timedelta(days=1)
            else:
                try:
                    endDate=datetime.strptime(endDate, dateFormat).date()
                    endDate+=timedelta(days=1)
                except Exception:
                    return {'Exception': 'Incorrect format for endDate. It should be "YYYY-MM-DD" or "today"'}
            
            try:
                startTime=datetime.strptime(startTime, timeFormat).time()
            except Exception:
                return {'Exception': 'Incorrect format for startTime. It should be "HH:MM'}
            
            try:
                endTime=datetime.strptime(endTime, timeFormat).time()
            except Exception:
                return {'Exception': 'Incorrect format for endTime. It should be "HH:MM"'}


            def daterange(start_date, end_date):
                for n in range(int((end_date - start_date).days)):
                    yield start_date + timedelta(n)

            #Triggering the Outlook application
            outlook=win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
            inbox=outlook.GetdefaultFolder(6)    #6 is the index for the inbox folder
            inboxMessages=inbox.Items
            
            #Creating an excel file
            writer=pandas.ExcelWriter(excelPath+'\\EmailsReceivedDailyReport.xlsx', engine='xlsxwriter')
            writer.save()            
            
            counter=0
            for singleDate in daterange(startDate, endDate):
                count=0
                for message in inboxMessages:
                    msgDate=message.SentOn.date()
                    msgTime1=message.SentOn.strftime(timeFormat)
                    msgTime=datetime.strptime(msgTime1, timeFormat).time()
                
                    if singleDate==msgDate:
                        if startTime<=msgTime<=endTime:
                            count+=1
                            #print(message.Subject)
                
                #Appending the data in the excel sheet created above
                dateRcvd=[str(singleDate)]
                countOfMsg=[count]
                df=DataFrame({'Date (YYYY-MM-DD)':dateRcvd,'CountOfReceivedEmails':countOfMsg})
                dfExcel=pandas.read_excel(excelPath+'\\EmailsReceivedDailyReport.xlsx')
                result=pandas.concat([dfExcel, df], ignore_index=True)
                result.to_excel(excelPath+'\\EmailsReceivedDailyReport.xlsx', index=False)
                
                counter+=1
                print('Number of emails received on '+str(singleDate)+': '+str(count))

            if counter!=0:
                return {'Status': 'Success'}
            else:
                return {'Exception': 'No emails found in the specified period'}



        except Exception as e:
            return {'Exception': str(e)}

if __name__=='__main__':
    context={}
    bot_obj=CountEmailsReceivedDailyInTimeRange()

    #enter the date in the format: 'YYYY-MM-DD'
    #for the current date, input dates can be provided as: 'Today'
    
    #enter the time in the 24 hrs format as: 'HH:MM'
    
    context={
            'startDate': '', 'endDate': '',     #enter dates between which daily report is to be generated
            'startTime': '', 'endTime': '',     #enter time for which the bot need to count the mails   
            'excelPath': ''                     #excel path is the location where you want to save the output excel file
            }

    '''
    #Sample Data for inputs:
    context={
            'startDate': '2020-07-07', 'endDate': 'Today', 
            'startTime': '00:00', 'endTime': '17:10',    
            'excelPath': 'C:\\Users\\vikas.singh09\\Desktop'
            }
    '''

    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)

