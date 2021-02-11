'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import json
import pysnow
import urllib.request
import win32com.client as win32
from abstract_bot import Bot


# Python Bot to send email

class SendReminderEmail(Bot):

	def bot_init(self):
		pass

	def execute(self, executeContext) :
		try:
			snowServerInstance = executeContext['snowServerInstance']
			if not snowServerInstance:
				return {'validation error' : 'missing argument snowServerInstance'}
			
			snowUsername = executeContext['snowUsername']
			if  not snowUsername:
				return {'validation error' : 'missing argument snowUsername'}
			
			snowPassword = executeContext['snowPassword']
			if not snowPassword:
				return {'validation error' : 'missing argument snowPassword'}
			
			instanceNumber = executeContext['instanceNumber']
			if  not instanceNumber:
				return {'validation error' : 'missing argument instanceNumber'}
			
			maxSendEmailCount = executeContext['maxSendEmailCount']
			if  not maxSendEmailCount:
				return {'validation error' : 'missing argument maxSendEmailCount'}
			
			sendTo = executeContext['sendTo']
			if  not sendTo:
				return {'validation error' : 'missing argument sendTo'}

			conn = pysnow.Client(instance=snowServerInstance, user=snowUsername, password=snowPassword)
			incident = conn.resource(api_path='/table/incident')
			incidentData =  incident.get(query={'number': instanceNumber}).one()
			incidentState = incidentData['incident_state']
			incidentSendEmailComment =   incidentData['description']  

			
			SendEmailCount = [int(s) for s in incidentSendEmailComment.split() if s.isdigit()]

			
			if int(incidentState) == 2:                       # Pending or in Progress
				if not SendEmailCount:
					sendNote = 'Reminder Email Sent 1 time'
					update = {'description': sendNote}
					updated_record = incident.update(query={'number': instanceNumber}, payload=update)
					print (sendNote)
					return {'send_email' : 'yes', 'status' : 'success', 'sendTo' :  sendTo, 'instanceNumber' : instanceNumber }
				else:
					newCount = int(SendEmailCount[0]) + 1
					if SendEmailCount[0] >= int(maxSendEmailCount):
						sendNote = 'Issue Closed'
						update = {'description': sendNote, 'state': 5}
						updated_record = incident.update(query={'number': instanceNumber}, payload=update)
						print (sendNote)
						return {'send_email' : 'no', 'status' : 'success'}
					else:
						sendNote = 'Reminder email sent {0} time'.format(newCount)
						update = {'description': sendNote}
						updated_record = incident.update(query={'number': instanceNumber}, payload=update)
						print (sendNote)
						return {'send_email' : 'yes', 'status' : 'success', 'sendTo' : sendTo, 'instanceNumber' : instanceNumber}
			return {'status' : 'success'}
		except Exception as e:
			return {'Exception' : str(e)}

  
if __name__ == '__main__':
	context = {}
	bot_obj = SendReminderEmail()

	context =  {
				# 'snowServerInstance' : 'dev82133',
				# 'snowUsername' : 'admin',
				# 'snowPassword' : 'Zainu01$$',
				# 'instanceNumber': 'INC0010007',
				# 'maxSendEmailCount' : '3',
				# 'sendTo' : 'vikram.chauhan@infosys.com',
				'snowServerInstance' : '',
				'snowUsername' : '',
				'snowPassword' : '',
				'instanceNumber': '',
				'maxSendEmailCount' : '',
				'sendTo' : ''
				}
	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print('output : ',output)