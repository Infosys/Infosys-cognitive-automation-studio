'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import win32com.client as win32
import pandas as pd
from files.abstract_bot import Bot


# Python Bot to send email

class SendEmailToMultipleReceipents(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:
            path = executeContext['path']
            sheetName = executeContext['sheetName']
            xls = pd.ExcelFile(path)
            dfs = xls.parse(sheet_name="email_team", header=None)
            recipients = []
            for i in dfs[0]:
                recipients.append(i)
            recipientsTo = ' ; '.join(recipients)
            print(recipientsTo)

            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = recipientsTo
            mail.Subject = 'Automatic Email '
            mail.Body = 'body'
            mail.HTMLBody = '<h2> Hello, this is a test for new project details. please respond venky garu. </h2>'
            mail.Send()
            return {'status': 'success'}
        except Exception as e:
            return {'Exception': str(e)}


if __name__ == '__main__':
    context = {}
    bot_obj = SendEmailToMultipleReceipents()
    context = {'filePath': '', 'sheetName': ''}
    output = bot_obj.execute(context)
    print(output)
