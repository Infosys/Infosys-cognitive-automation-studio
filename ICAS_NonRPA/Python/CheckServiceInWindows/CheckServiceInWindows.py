'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import wmi
from socket import *
from abstract_bot import Bot

# Bot to check the status of service running on window server 

class CheckServiceInWindows(Bot):
	
	def bot_init(self):
		pass

		
	def execute(self,executionContext):
	
		try:
			ipAddress = executionContext['ipAddress']
			if not ipAddress:
				return {'validation' :  'Enter a valid IP Address'}
			username = executionContext['username']
			if not username:
				return {'validation' :  'Enter a valid username'}
			password = executionContext['password']
			if not password:
				return {'validation' :  'Enter a valid password'}
			serviceName = executionContext['serviceName']
			if not serviceName:
				return {'validation' :  'Enter a valid service name '}

			print('Establishing connection to {0}'.format(ipAddress))
			print('Username: {0}'.format(username))
			connection = wmi.WMI(ipAddress, user = username, password = password)
			print('Connection established')
			
			output = ''
			for service in connection.Win32_Service():
				if service.Name == serviceName:
					serviceState = '{0}'.format(service.State)
					output = {'status' : serviceState} 
					return output
					break
			else:
				return { "status" : "Service name is either Invalid or Service Not Found"}	
		except Exception as e:
			print('Your Username and Password of '+getfqdn(ipAddress)+' are wrong.')
			return {'Exception' : str(e)}
	

if __name__ == "__main__":
	context = {}
	bot_obj = CheckServiceInWindows()

	context = {'ipAddress':'',
				'username':'',
				'password':'',
				'serviceName' : ''
				}

	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print(output)  
