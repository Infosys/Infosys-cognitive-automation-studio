'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#dependencies to be installed before running
import socket
from abstract_bot import Bot

#bot to check whether a port is open or not (For windows as well as linux server)
class PortCheck(Bot):
    def bot_init_(self):
        pass
    def execute(self,executionContext):
        try:   
            var_server_name=executionContext['var_server_name']
            var_port_number=executionContext['var_port_number']
            
            if var_server_name is None:
                return ("Missing Arguments: Server Name")
            if var_port_number is None:
                return ("Missing Arguments: port_number")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)                                      #2 Second Timeout
            result = sock.connect_ex((var_server_name,int(var_port_number)))
            if result == 0:
                return {'Status':'Port is OPEN'}
            else:
                return {'Status':'Port is CLOSED, The connect_ex return code is '+str(result)}
            
        except socket.error:
            return{'Error':'Could not connect to a server'}
        except socket.gaierror:
            return{'Error':'Hostname could not be resolved'}
        finally:
            sock.close()
            
if __name__ == "__main__":
    context = {}
    bot_obj = PortCheck()

    context = {'var_server_name':'', #enter ip address
               'var_port_number':''  #enter port number 
               }
			   
    output = bot_obj.execute(context)
    print(output)     
            
                