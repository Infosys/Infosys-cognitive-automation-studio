'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
from win32com.client import Dispatch
import datetime


class CountOfEmailAddressesForSpecificTime(Bot):

    def bot_init_(self):
        pass

    def execute(self, executeContext):
        try:
            countOfEmails = 0
            toTime = executeContext['toTime']
            fromDate = executeContext['fromDate']

            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            SentItems = outlook.GetDefaultFolder(5)
            emails = SentItems.Items
            recipients = []
            emails.Sort("[SentOn]", True)

            Date = datetime.datetime.strptime(fromDate, '%m/%d/%Y %H:%M')

            toTime = datetime.datetime.strptime(toTime, '%m/%d/%Y %H:%M')

            emailsInTimeRange = emails.Restrict(
                "[SentOn] >= '" + Date.strftime("%m/%d/%Y %H:%M") + "' AND [SentOn] < '" + toTime.strftime(
                    "%m/%d/%Y %H:%M") + "'")

            for email in emailsInTimeRange:
                for sm in emailsInTimeRange:
                    if sm.Class == 43:
                        if sm.To not in recipients:
                            recipients.append(sm.To)
                countOfEmails+=1



            output = 'Total number of sent email addresses are ' + str(len(recipients))
            return {'Status': output}
        except Exception as e:
            return {'Exception': str(e)}


if __name__ == '__main__':
    # context = {'toTime':'07/07/2020 17:00','fromDate':'06/15/2020 09:00'} Date & Time in MM/DD/YYYY HH:MM format
    context = {'toTime': '07/13/2020 16:53', 'fromDate': '07/13/2020 09:00'}
    obj = CountOfEmailAddressesForSpecificTime()
    output = obj.execute(context)
    print(output)
