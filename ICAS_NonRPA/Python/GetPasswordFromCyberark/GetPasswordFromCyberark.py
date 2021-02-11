'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

from pyaim import CCPPasswordREST
from abstract_bot import Bot

# Python bot to get password of a user from cyberark

class GetPasswordFromCyberark(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            serverName = executeContext['serverName']
            appID = executeContext['appID']
            safeName = executeContext['safeName']
            userName=executeContext['userName']
                        
            if serverName =='':
                return{'Missing Argument':'serverName'}
            if appID =='':
                return{'Missing Argument':'appID'}
            if safeName =='':
                return{'Missing Argument':'safeName'}
            if userName =='':
                return{'Missing Argument':'userName'}
            
            #establishing the connection
            aimccp = CCPPasswordREST(serverName, verify=True) # set verify=False to ignore SSL
            service_status = aimccp.check_service()
            
            if service_status == 'SUCCESS: AIMWebService Found. Status Code: 200':
                response = aimccp.GetPassword(appid=appID,safe=safeName,username=userName)
                print('Full Python Object: {}'.format(response))
                return{'Password' : '{}'.format(response['Content'])}
            else:
                raise Exception(service_status)
            
        except Exception as e:
            return{'Exception' : str(e)}

  
if __name__ == '__main__':
    context = {}
    bot_obj = GetPasswordFromCyberark()

    context = {'serverName':'', #Enter the cyberark url like : https://ccp.cyberarkdemo.example
               'appID':'',
               'safeName':'',
               'userName':''}
    
    
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
