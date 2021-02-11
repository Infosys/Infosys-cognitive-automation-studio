'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from files.abstract_bot import Bot
from win32com.client import Dispatch
import datetime as dt

# Bot to count the number of emails received within a given time period
# Input Parameters: fromTime - datetime from which emails are to be counted
#                   toTime - datetime till which emails are to be counted
# Returns success status and count of the emails received between the timeframe


class CountEmailsReceivedInTimeRange(Bot):

    def bot_init_(self):
        pass

    def execute(self, executeContext):
        try:
            countOfEmails = 0
            inputFromTime = executeContext['fromTime']
            inputToTime = executeContext['toTime']

            if inputFromTime == "" or inputToTime == "":

                raise Exception('input datetime is incorrect')

            else:
                outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
                inbox = outlook.getDefaultFolder("6")
                emails = inbox.Items
                emails.Sort("[ReceivedTime]", True)
                fromTimeStr = dt.datetime.strptime(inputFromTime,'%m/%d/%Y %H:%M')
                
                toTimeStr = dt.datetime.strptime(inputToTime, '%m/%d/%Y %H:%M')
                emailsInTimeRange = emails.Restrict("[ReceivedTime] >= '" + fromTimeStr.strftime("%m/%d/%Y %H:%M") + "' AND [ReceivedTime] < '" +toTimeStr.strftime("%m/%d/%Y %H:%M") + "'")

                for email in emailsInTimeRange:
                    countOfEmails += 1

                return {'status':'success. {} emails received between {} and {}'.format(countOfEmails, fromTimeStr, toTimeStr)}
        except Exception as e:
            return {'Exception': str(e)}


if __name__ == '__main__':
    context = {'fromTime': '', 'toTime': ''}
    #context = {'fromTime':'05/30/2020', 'toTime':'07/12/2020 00:01'}
    obj = CountEmailsReceivedInTimeRange()
    output = obj.execute(context)
    print(output)
