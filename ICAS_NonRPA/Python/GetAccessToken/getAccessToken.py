'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import requests

class GetAccessToken(Bot):

    def bot_init(self):
        pass
    
            
    def execute(self, executeContext):
        

        try:
            serverName = executeContext['serverName']
            userName = executeContext['userName']
            password = executeContext['password']
            
                #        r = requests.get(url = "https://vimppnz02-01:8443/cas/oauth2.0/accessToken?grant_type=password&client_id=clientid&username=apiuser&password=apikey",verify=False) 
            r = requests.get(url = "https://"+serverName+":8443/cas/oauth2.0/accessToken?grant_type=password&client_id=clientid&username="+userName+"&password="+password+"",verify=False) 
            
            accesToken=str(r.content)
            accesToken=accesToken.split("&")
                    
            accesToken=accesToken[0].split("=")
                    
            accesToken='Bearer '+accesToken[1]
                    
            return {'accessToken':accesToken}
                
        except Exception as e:
                
                return {'Exception':str(e)}

if __name__ == '__main__':
    context = {}
    bot_obj = GetAccessToken()
    context = {'serverName':'','userName':'','password':''}
#    context = {'serverName':'vimppnz02-01','userName':'apiuser','password':'apikey'} # Nia url to get the access Token 
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
