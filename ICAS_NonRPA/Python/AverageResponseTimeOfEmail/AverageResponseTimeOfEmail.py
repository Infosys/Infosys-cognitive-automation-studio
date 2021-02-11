'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from files.abstract_bot import Bot
from win32com.client import Dispatch
import datetime

class AverageResponseTimeOfEmail(Bot):

    def bot_init_(self):
        pass

    def execute(self, executeContext):
        try:
            toTime = executeContext['toTime']
            fromDate = executeContext['fromDate']
            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            inbox = outlook.GetDefaultFolder(6)
            inboxMsgs = inbox.Items
            receivedTime = ""
            sentTime = ""
            countOfEmails = 0
            sumOfRespTime = 0
            fromDate=datetime.datetime.strptime(fromDate,'%m/%d/%Y %H:%M')
            toTime=datetime.datetime.strptime(toTime, '%m/%d/%Y %H:%M')
            
            receivedEmailsInTimeRange = inboxMsgs.Restrict("[ReceivedTime] >= '" + fromDate.strftime("%m/%d/%Y %H:%M") + "' AND [ReceivedTime] < '" +toTime.strftime("%m/%d/%Y %H:%M") + "'")
            for email in receivedEmailsInTimeRange:
                mailSubject = email.subject
                receivedTime = email.ReceivedTime
                sentItems = outlook.GetDefaultFolder(5)
                sentMsgs = sentItems.Items
                sentEmailsInTimeRange = sentMsgs.Restrict("[SentOn] >= '" + fromDate.strftime("%m/%d/%Y %H:%M") + "' AND [SentOn] < '" +toTime.strftime("%m/%d/%Y %H:%M") + "'")
                for mail in sentEmailsInTimeRange:
                    if mail.subject == "RE: "+mailSubject:
                        sentTime = mail.SentOn
                        countOfEmails += 1
                        break
                    else:
                        sentTime = receivedTime


                diff = sentTime - receivedTime
                minutes = divmod(diff.seconds, 60)
#                print("difference is....",minutes[0],countOfEmails)
                sumOfRespTime +=minutes[0]
                            
            print(sumOfRespTime,countOfEmails)
            print(countOfEmails)
            avgRespTime = sumOfRespTime/countOfEmails
#            print("Average Response Time is {} minutes".format(avgRespTime))
            return {'Status':'Success','AverageResponseTime': str(avgRespTime)+" minutes"}
        except Exception as e:
            return {'Exception': str(e)}


if __name__ == '__main__':
    
    context = {}
    bot_obj = AverageResponseTimeOfEmail()
#    context = {'fromDate':'07/09/2020 22:00','toTime':'07/08/2020 00:00'}
    context = {'fromDate':'','toTime':''}
    output = bot_obj.execute(context)
    print(output)
