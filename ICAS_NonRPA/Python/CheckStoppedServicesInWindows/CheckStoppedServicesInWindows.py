'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import wmi
import csv
from abstract_bot import Bot

class CheckStoppedServicesInWindows(Bot):
	
	def bot_init(self):
		pass

		
	def execute(self,executionContext):
            ipAddress = executionContext['ipAddress']
            fileName = executionContext['fileName']
            userName = executionContext['userName']
            password = executionContext['password']
            filePath = executionContext['filePath']
		

            try:
                connection = wmi.WMI(ipAddress, user = userName, password = password) #connecting with a remote server
                print('Connection established')
                for s in connection.Win32_Service():
                        if s.State == "Stopped":
                            with open(filePath + fileName, 'a', newline='') as csvoutput:
                                output = csv.writer(csvoutput)
                                output.writerow([s.Name])
                return {"output":"success"}

			
            except Exception as e:
                return {'Exception' : str(e)}
	

if __name__ == "__main__":
	context = {}
	bot_obj = CheckStoppedServicesInWindows()

	context = {'ipAddress':'',
				'userName':'',
				'password':'',
				'filePath':'',
                'fileName':''
				
				}

	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print(output)  
