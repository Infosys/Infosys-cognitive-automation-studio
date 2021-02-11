'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import win32com.client as win32
from abstract_bot import Bot
import json
import urllib.request

class SendEmail(Bot):

  
    def execute(self, executeContext) :
        try:
            import win32com.client as win32
            outlook = win32.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
        
            mail_type=executeContext['mail_status_code']
            mail.To = executeContext['send_to']
            print(mail_type, mail.To)
            
             
            if int(mail_type) == 1:
                # HtmlFile = open('file_not_found.html','r',encoding='utf-8')
                # body = str(HtmlFile.read())
                body =  """
                            <!DOCTYPE html>\n<html>\n<body>\n<p> Hello user, </p>\n<p>
                            The location of file is either invalid or File not found.</p>\n<br>\n<p>
                            Thanks,</p>\n<p>Team Impact</p>\n</body>\n</html>\n\n
                        """
                mail.HTMLBody = body
                mail.Subject = 'File not Found'
                mail.send
            elif int(mail_type) == 2:
                body =  """
                            <!DOCTYPE html>\n<html>\n<body>\n<p> Hello user, </p>\n<p>
                            File received after 05:00 AM.</p>\n<br>\n<p>
                            Thanks,</p>\n<p>Team Impact</p>\n</body>\n</html>\n\n
                        """
                mail.HTMLBody = body
                mail.Subject = 'File received after 5 AM'
                mail.send
            elif int(mail_type) == 3:
                body =  """
                            <!DOCTYPE html>\n<html>\n<body>\n<p> Hello user, </p>\n<p>
                            The length of some Records in file is invalid. Each record must be of size 172 Bytes.</p>\n<br>\n<p>
                            Thanks,</p>\n<p>Team Impact</p>\n</body>\n</html>\n\n
                        """
                mail.HTMLBody = body
                mail.Subject = 'Invalid Record Size Length'
                mail.send
            
            # print('type of body is:',type(body))
            return {'success':'Mail sent successfully'}
            #return {'Random forest pickle':json.dumps('success')}
        except Exception as e:
            print("Error occured in LGB ",str(e)) 
            return{'Exception': str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = SendEmail()

    context = {
                'send_to':'', 'mail_status_code' : ''
        }
    bot_obj.bot_init()
    print (context)

    resp = bot_obj.execute(context)
    print('response : ',resp)