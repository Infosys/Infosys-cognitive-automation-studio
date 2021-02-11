'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import wmi
from socket import *
from abstract_bot import Bot

#Bot to check the status of windows disk space

class CheckDiskspaceInWindows(Bot):
	
	def bot_init(self):
		pass

		
	def execute(self,executionContext):
		ipAddress = executionContext['ipAddress']
		userName = executionContext['userName']
		password = executionContext['password']

		try:
			print('Establishing connection to {0}'.format(ipAddress))
			print('userName: {0}'.format(userName))
			connection = wmi.WMI(ipAddress, user = userName, password = password)  #to connect with a remote server
			print('Connection established')
            
            #to check the disk stats
			
			for disk in connection.Win32_LogicalDisk():
				if disk.size!=None:
					diskFreePercentage="{0:.2f}% free".format(100*float(disk.FreeSpace)/float(disk.Size))
                    
					print(disk.Caption) #prints the name of the disk
					print(disk.Size) #prints the total size of the disk in bytes
					
					finalStats='FreeDiskSpace: '+disk.FreeSpace+'bytes '+'DiskFreePercent: '+diskFreePercentage  #Free disk size is in bytes
					return {'Output':finalStats}
				 
				"""
				#add this code to compare the freediskspace of the drive with a particular required size
					
					print(disk.FreeSpace) #prints the free disk size in bytes
					
					if float(disk.FreeSpace)>200: #any other size in bytes can be provided for comparison
						result='Sufficient DiskSpace'
						output={'result':result}
					else:
						result='Insufficient DiskSpace'
						output={'result':result}
					return output
				"""
             
		except Exception as e:
			print('Your userName and Password of '+getfqdn(ipAddress)+' are wrong.')
			return {'Exception' : str(e)}
	

if __name__ == "__main__":
	context = {}
	bot_obj = CheckDiskspaceInWindows()

	context = {'ipAddress':'',
				'userName':'',
				'password':''
				}

	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print(output)  
