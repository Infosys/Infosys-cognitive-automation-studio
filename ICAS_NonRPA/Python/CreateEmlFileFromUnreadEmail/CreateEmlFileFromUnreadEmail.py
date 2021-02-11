'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import time
import traceback
import sys
import json
from email import generator
from abstract_bot import Bot    
from ast import literal_eval
from email.mime.multipart import MIMEMultipart 

# Python Bot to create .eml file


class CreateEmlFile(Bot):

	def bot_init(self):
		pass
		
	def execute(self, executeContext) :
		try:
			emlFolderPath = executeContext['emlFolderPath']
			if not emlFolderPath:
				return {'validation error' : 'missing argument emlFolderPath'}
			
			emailData = executeContext['emailData']
			if  not emailData:
				return {'validation error' : 'missing argument emailData'}

			emailData = json.loads(emailData) 
			
			emlFiles = []
			for email in emailData:
				msg = MIMEMultipart('alternative')
				msg['Subject'] = email['Subject']
				msg['Sender'] = email['Sender']
				
				body = email['Body']
				# creating body after truncating string to remove(header inside header)
				trucnate_part = body.find('Subject') 
				search_index = 0   
				if trucnate_part >= 1:
					search_index = trucnate_part
					emailBody = body[search_index:]
					msg['Body']  = emailBody
				else:
					msg['Body']  = body.encode('ascii',errors='ignore').decode('ascii')
			   
			
				# creating emlFileName
				timestamp = str(time.time())
				timestamp = timestamp.replace('.','_')
				emlFileName  = emlFolderPath + '\\' + timestamp + '.eml'
				emlFiles.append(emlFileName)
				with open(emlFileName, 'w') as outfile:
					gen = generator.Generator(outfile)
					gen.flatten(msg)       
				
			return {'mailList': emlFiles}  
		except Exception as e:
			return {'Exception': str(e)}

	   
	
if __name__ == '__main__':
	context = {}
	bot_obj = CreateEmlFile()

	context = {
				'emlFolderPath' :  "",
				'emailData' : ""

				# 'emlFolderPath' :  "D:\JAVATEST",
				# 'emailData' : '[{"Sender": "Vikram Chauhan", "Subject": "Test Email", "Body": "Hello How are you"}]'
				
			}
			
	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print('output : ',output)