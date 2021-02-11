'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from files.abstract_bot import Bot
from win32com.client import Dispatch
import pandas as pd
import datetime
from collections import Counter
import json

class CountHourlyEmailsWithBusiestHourSentInTimeRange():

    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:
            countOfEmails = 0
            toTime = executeContext['toTime']
            fromDate = executeContext['fromDate']
            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            SentItems = outlook.GetDefaultFolder(5)           
            emails = SentItems.Items
            emails.Sort("[SentOn]", True)

            Date=datetime.datetime.strptime(fromDate,'%m/%d/%Y %H:%M')            
            toTime=datetime.datetime.strptime(toTime, '%m/%d/%Y %H:%M')

            emailsInTimeRange = emails.Restrict("[SentOn] >= '" + Date.strftime("%m/%d/%Y %H:%M") + "' AND [SentOn] < '" +toTime.strftime("%m/%d/%Y %H:%M") + "'")

            dates= []           
            for email in emailsInTimeRange:
                temp_date=datetime.datetime.strptime(str(email.SentOn)[:-12],'%Y-%m-%d %H')
                temp_date= str(temp_date)[:-6]
                dates.append(temp_date)
   
            temp_dict= dict(Counter(dates))
            df= pd.DataFrame()
            df['SentHour']= [x.split(" ")[1] for x in temp_dict.keys()]
            df['SentDate']= [x.split(" ")[0] for x in temp_dict.keys()]
            df['count']=temp_dict.values()
            temp_df= df.sort_values(by=['count'], ascending=False).reset_index(drop= True)

            busiestHour= temp_df['SentDate'][0] + " " + temp_df['SentHour'][0]
            busiestHourEmails= temp_df['count'][0]
            
#            print(busiestHour,"Number of emails : " ,busiestHourEmails, "Done")           
#            print("You have sent {} emails between {} and {} ".format(countOfEmails,Date,toTime))
            return {'Status':'Success', 'CountOfSentEmailsHourly': df.to_json(), 'busiestHour':busiestHour, 'busiestHourEmailsCount': str(busiestHourEmails)}
        except Exception as e:
            return {'Exception': str(e)}


if __name__ == '__main__':
#    context = {'toTime':'07/10/2020 17:00', 'fromDate':'05/01/2020 09:00'} #Date & Time in MM/DD/YYYY HH:MM format
    context = {'toTime':'','fromDate':''}
    obj = CountHourlyEmailsWithBusiestHourSentInTimeRange()
    obj.bot_init()
    output = obj.execute(context)
    print(output)