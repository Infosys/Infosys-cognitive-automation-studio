'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import csv
import subprocess
import pandas as pd
from abstract_bot import Bot

#class for bot
class TestServersListStatus(Bot):
    
    def bot_init(self):
        pass
   
    def execute(self,executionContext):
        try:
            fileInputPath =executionContext["fileInputPath"]
            fileOutputPath=executionContext["fileOutputPath"]
            hostname = pd.read_csv(fileInputPath)
            host_names = hostname.values.tolist()
            
            for server in host_names:
                response = subprocess.Popen(['ping',server[0]],stdout = subprocess.PIPE).communicate()[0]
                response = response.decode()
                print(response)
                if 'bytes=32' in response:
                    status = 'Up'
                elif 'destination host unreachable' in response:
                        status = 'Unreachable'
                else:
                    status = 'Down'
    
                with open(fileOutputPath, 'a', newline='') as csvoutput:
                    output = csv.writer(csvoutput)
                    output.writerow([server] + [status])
            
            return {"output":"success"}

			
            
        except Exception as e:
          return {'Exception' : str(e)} 

if __name__ == "__main__":
	context = {}
	bot_obj = TestServersListStatus()

	context = {'fileInputPath':'',
				'fileOutputPath':''
				}

	bot_obj.bot_init()
	output = bot_obj.execute(context)
	print(output)  
