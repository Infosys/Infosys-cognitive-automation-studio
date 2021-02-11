'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from win32com.client import Dispatch
from datetime import datetime
import datetime as dt
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot to calculate the least amount of time user took to respond to an email during the selected period.
class LeastTimeTookToRespondAnEmail(Bot):
    
    def bot_init_(self):
        pass

    def execute(self,executionContext):
        try:    
            startDate=executionContext['startDate']
            endDate=executionContext['endDate']
            
            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            sent = outlook.GetDefaultFolder(5)
            smessages = sent.Items
            inbox = outlook.GetDefaultFolder(6)
            rmessages = inbox.Items
            w = datetime.strptime(startDate, '%d/%m/%Y')
            x = datetime.strptime(endDate, '%d/%m/%Y')
            time = []
            for rm in rmessages:
                rmfdate = rm.ReceivedTime.strftime('%d/%m/%Y')
                rmpdate = datetime.strptime(rmfdate, '%d/%m/%Y')
                for sm in smessages:
                    smfdate = sm.SentOn.strftime('%d/%m/%Y')
                    smpdate = datetime.strptime(smfdate, '%d/%m/%Y')
                    if (w <= rmpdate <= x) and (w <= smpdate <= x):
                        if rm.Subject == sm.Subject.split(': ')[-1]:
                            if sm.SentOn > rm.ReceivedTime:
                                time.append((sm.SentOn - rm.ReceivedTime).total_seconds())
                        if rm.Subject == sm.Subject:
                            if sm.SentOn > rm.ReceivedTime:
                                time.append((sm.SentOn - rm.ReceivedTime).total_seconds())
                        if rm.Subject.split(': ')[-1] == sm.Subject.split(': ')[-1]:
                            if sm.SentOn > rm.ReceivedTime:
                                time.append((sm.SentOn - rm.ReceivedTime).total_seconds())
            if len(time) != 0:
                mtime = round(min(time))
                otime = str(dt.timedelta(seconds = mtime))
                output = 'The least amount of time user took to respond to an email during '+startDate+' and '+endDate+' is '+ otime
                return {'Status': output}
            else:
                return {'Status': 'No record found'}
        except Exception as e:
            return {'Exception': str(e)}
    
if __name__ == "__main__":
    context = {}
    bot_obj = LeastTimeTookToRespondAnEmail()
 
    context = {'startDate':'',      #07/07/2020  (DD/MM/YYYY)
               'endDate':'',        #07/07/2020  (DD/MM/YYYY)
               }

    output = bot_obj.execute(context)
    print(output)    