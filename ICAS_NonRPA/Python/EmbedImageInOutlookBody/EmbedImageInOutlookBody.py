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

class EmbedImageInOutlookBody(Bot):

	def bot_init(self):
		pass

	def execute(self, executeContext) :
		try:
			mail_to = executeContext['send_to']
			if not mail_to:
				return {'Exception' : 'missing argument send_to'}
			
			image = executeContext['image']
			if not image:
				return {'Exception' : 'missing argument image'}

			outlook = win32.Dispatch('outlook.application')
			mail = outlook.CreateItem(0)

			attachment = mail.Attachments.Add(image)
			attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "MyId1")
			mail.HTMLBody = "<html><body>Test image <img src=""cid:MyId1""></body></html>"
			
			mail.To = mail_to
			mail.Subject = 'Image File Received'
			mail.send
			return {'status' : 'success'}
		except Exception as e:
			return {'Exception' : str(e)}

  
if __name__ == '__main__':
	context = {}
	bot_obj = EmbedImageInOutlookBody()

	context =  {
				'send_to': '', 
				'image' : ''
				
				}
	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print('output : ',output)