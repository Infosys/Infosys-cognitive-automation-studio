'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import traceback
import sys
from abstract_bot import Bot
from socket import getfqdn
import wmi

class StartServiceInWindows(Bot):
	def bot_init(self):
		pass
		
	def execute(self,executeContext):
		userName=executeContext['userName']
		password=executeContext['password']
		serviceName=executeContext['serviceName']
		try:
			virtualMachineIp=executeContext['virtualMachineIp']
			print('Virtual Machine IP: {0}'.format(virtualMachineIp))
			self.virtualMachineIp = virtualMachineIp
			print('Establishing connection to {0}'.format(self.virtualMachineIp))
			print('Username: {0}'.format(userName))
			connection = wmi.WMI(self.virtualMachineIp, user = userName, password = password)
			print('Connection established')
			serviceFound=False
			for service in connection.Win32_Service():
			    #print(serviceName)
				if service.Name == serviceName:
					serviceFound=True
					service.StartService()	
			if serviceFound == False:
			    return{'status':'service not found'}
			else:
				return{'status':'service started'}					
		except wmi.x_wmi:
			return{'Exception': getfqdn(self.virtualMachineIp)+' are wrong.'}
	

		
	
if __name__=="__main__":
    context={}
    bot_obj=StartServiceInWindows()
#    context = {'virtualMachineIp':'','userName':'','password':'','serviceName':'Themes'}
    context = {'virtualMachineIp':'','userName':'','password':'','serviceName':''}
    
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)