'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import socket
from abstract_bot import Bot

class CheckPorts(Bot):
    def bot_init_(self):
        pass
    def execute(self,executionContext):
        try:   
            serverName=executionContext['serverName']
            portNumber=executionContext['portNumber']
                  
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)                                      #2 Second Timeout
            result = sock.connect_ex((serverName,int(portNumber)))
            if result == 0:
                return {'Status':'Port is OPEN'}
            else:
                return {'Status':'Port is CLOSED, The connect_ex return code is '+str(result)}
            
            sock.close()
            
        except Exception as e:
            return {'Exception':str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = CheckPorts()

    context = {'serverName':'',
               'portNumber':'' 
               }

   
    output = bot_obj.execute(context)
    print(output)     
            
                