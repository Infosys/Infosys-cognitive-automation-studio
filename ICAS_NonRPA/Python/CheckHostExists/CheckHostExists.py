'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import socket
from abstract_bot import Bot

class CheckHostExists(Bot):

    def bot_init(self):
        pass
        
    def execute(self, executeContext):
        try:
            serverName = executeContext['serverName']
            result =  socket.gethostbyname(serverName)
            if result:
                return {'Output':"Host exists with Ip: "+result}
#            else:
#                 return {'Output':"Host does not exist"}
                
        except Exception as e:
             return {'Exception':str(e)}
   

if __name__ == '__main__':

    context = {}
    bot_obj = CheckHostExists()
#    context = {'serverName' :'vimphyz03-01'}
    context = {'serverName' :''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
