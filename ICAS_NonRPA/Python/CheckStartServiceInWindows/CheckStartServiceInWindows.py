'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import wmi
class CheckStartServiceInWindows():

	def bot_init(self):
		pass

	def execute(self,executionContext):
		serverName = executionContext['serverName']
		userName = executionContext['userName']
		password = executionContext['password']
		serviceName = executionContext['serviceName']

		try:
			if serverName == '':
				return ("Missing argument : serverName")
			if userName == '':
				return ("Missing argument : userName")
			if  password == '':
				return ("Missing argument :password")

			print('Establishing connection to {0}'.format(serverName))
			print('Username: {0}'.format(userName))
			connection = wmi.WMI(serverName, user = userName, password = password)
			print('Connection established')

			for service in connection.Win32_Service():
				print(service.Name +"       State        " + service.State)
				if service.Name == serviceName:
					serviceState = '{0}'.format(service.State)
					if serviceState == 'Running':
						return {'Status' : "Service is already running"}
					else:
						service.StartService()
						return{'status' : "Service has now been started"}
			
		except Exception as e:
			return {'Exception' : str(e)}


if __name__ == "__main__":
	context = {}
	bot_obj = CheckStartServiceInWindows()
	context = {'serverName':'','userName':'','password':'','serviceName' :''}
	bot_obj.bot_init()
	OutputString = bot_obj.execute(context)
	print(OutputString)  
