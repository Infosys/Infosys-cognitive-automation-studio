'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import json
import urllib.request
import win32com.client as win32
from abstract_bot import Bot


# Python Bot to send email

class SendEmail(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext) :
        try:
            mail_to = executeContext['send_to']
            if not mail_to:
                return {'Exception' : 'missing argument send_to'}

            instanceNumber = executeContext['instanceNumber']
            if not instanceNumber:
                return {'Exception' : 'missing argument instanceNumber'}

            accounts= win32.Dispatch("Outlook.Application").Session.Accounts;
            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            
            
            body =  """
                        <!DOCTYPE html>\n<html>\n<body>\n<p> Hello user, </p>\n<p>
                        Please work on your issue , INCIDENT ID {0}. It is still pending.</p>\n<br>\n<p>
                        Thanks,</p>\n<p>Team Impact</p>\n</body>\n</html>\n\n
                    """.format(instanceNumber)
            mail.HTMLBody = body
            mail.To = mail_to
            mail.Subject = 'Issue In Progress'
            mail.send
            return {'status' : 'success'}
        except Exception as e:
            return {'Exception' : str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = SendEmail()

    context =  {
                'send_to': '', 
                'instanceNumber' : ''
                }
    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)