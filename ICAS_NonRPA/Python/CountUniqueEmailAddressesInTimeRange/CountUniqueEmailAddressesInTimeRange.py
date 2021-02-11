'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
from win32com.client import Dispatch
import datetime as dt

# Bot to count the number of unique email addresses that sent user an email within a given time period
# Input Parameters: fromTime - Date and time from which email addresses are to be counted
#                   toTime -   Date and time till which email addresses are to be counted
# Returns count of the unique email addresses and success status


class CountUniqueEmailAddressesInTimeRange(Bot):

    def bot_init_(self):
        pass

    def execute(self, executeContext):
        try:
            countOfEmailsAddress = 0
            uniqueEmailAddress = set()
            inputFromTime = executeContext['fromTime']
            inputToTime = executeContext['toTime']
            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            inbox = outlook.getDefaultFolder("6")
            emails = inbox.Items
            emails.Sort("[ReceivedTime]", True)
            fromTimeStr = dt.datetime.strptime(inputFromTime,'%m/%d/%Y %H:%M')
            
            toTimeStr = dt.datetime.strptime(inputToTime, '%m/%d/%Y %H:%M')

            emailsInTimeRange = emails.Restrict("[ReceivedTime] >= '" + fromTimeStr.strftime("%m/%d/%Y %H:%M") + "' AND [ReceivedTime] < '" +toTimeStr.strftime("%m/%d/%Y %H:%M") + "'")

            for email in emailsInTimeRange:
                if email.Class == 43 and email.SenderEmailType == 'EX':
                    uniqueEmailAddress.add(email.Sender.GetExchangeUser().PrimarySmtpAddress)
                else:
                    uniqueEmailAddress.add(email.SenderEmailAddress)
            
            countOfEmailsAddress = len(uniqueEmailAddress)

            return {'status':'success. {} different email addresses sent you emails between {} and {}'.format(countOfEmailsAddress, fromTimeStr, toTimeStr)}
        except Exception as e:
            return {'Exception': str(e)}


if __name__ == '__main__':
    #context = {'fromTime':'07/13/2020 00:01', 'toTime':'07/15/2020 00:01'}
    context = {'fromTime':'', 'toTime':''}
    obj = CountUniqueEmailAddressesInTimeRange()
    output = obj.execute(context)
    print(output)
