'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import win32com.client
import pandas as pd
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
#Bot to read polling emails from outlook and then calculate ratio of the responses
class CollateSurveyemailsToExcel(Bot):

    def bot_init(self):
        pass

    def execute(self,executionContext):
        try:
            subjectText = executionContext['subjectText']
            outputFile = executionContext['outputFile'] #Path of the output file with filename with .xlsx extension
            outlook = win32com.client.Dispatch('Outlook.Application').GetNamespace("MAPI") #Create outlook object
            inbox = outlook.GetDefaultFolder(6)
            mails = inbox.Items
            mailList = []
            mailSubject = ': '+subjectText
            for message in mails:
                messageList = []
                reply = message.Subject
                if mailSubject in message.Subject:
                    reply = message.Subject.replace(mailSubject,'')
                    if reply!='RE' and reply!='FW':
                        messageList.append(str(message.Sender))
                        messageList.append(message.Subject)
                        messageList.append(reply)
                        mailList.append(messageList)
            sender = []
            subject = []
            response = []
            for mail in mailList:
                sender.append(mail[0])
                subject.append(mail[1])
                response.append(mail[2])
            df = pd.DataFrame({'Sender':sender,'Subject':subject,'Response':response})
            writer = pd.ExcelWriter(outputFile, engine = 'xlsxwriter')
            df.to_excel(writer, sheet_name = subjectText )
            writer.save()
            df1 = pd.read_excel(outputFile)
            questions = df1.columns.ravel()
            result = []
            for i in range(3,len(questions)):
                output = df1[questions[i]].value_counts(normalize='true') 
                result.append(questions[i])
                result.append(output.to_string())
            return {'Response': result}
        except Exception as e:
            return {'Exception' : str(e)} 

if __name__ == "__main__":
    context = {}
    bot_obj = CollateSurveyemailsToExcel()
    context = {'subjectText' : '','outputFile' : ''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
