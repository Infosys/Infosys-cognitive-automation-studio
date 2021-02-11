'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os       
from abstract_bot import Bot #importing the Botclass from the abstract_bot.py
from socket import *
#Bot to check the status of a server
class TestServerstatus(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        try:
            serverName = executionContext["serverName"] #IP address of other remote server
            if serverName is None:
                return {'Missing Argument':'serverName'}
            remote_machine = (getfqdn(serverName)) #Method to get the name of the server using IP
            ping_response = os.popen(f"ping {serverName} -n 1").read() #Method to send and receive packet
            if "Received = 1" and "Approximate" in ping_response:
                state = 'Ping Successful with ' + remote_machine + ' having IP ' + serverName
                return {'State' : state}
            else:
                state = 'Ping Unsuccessful with ' + remote_machine + ' having IP ' + serverName
                return {'State' : state}
        except Exception as e:
            return {'Exception' : str(e)}
        
if __name__ == "__main__":
    context = {}
    bot_obj = TestServerstatus()
    context = {'serverName':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)