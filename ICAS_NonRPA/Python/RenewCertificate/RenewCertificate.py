'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import paramiko
import json
from abstract_bot import Bot

#class for bot
class RenewCertificate(Bot):
    #method to initialise 
    def bot_init(self):
        pass
   
    def execute(self,executionContext):
        try:
            serverName =executionContext['serverName']
            userName=executionContext['userName']
            password=executionContext['password']
            importKeystorePath=executionContext['importKeystorePath']
            keyPath=executionContext['keyPath']
            aliasName=executionContext['aliasName']
            storePass=executionContext['storePass']
            importCertName=executionContext['importCertName']
            
            
            if serverName is None:
                return ("Missing argument : serverName")
            if userName is None:
                return ("Missing argument : userName")
            if  password is None:
                return ("Missing argument :password")

            # connecting to server
            ssh=paramiko.SSHClient()
            importCommand='sudo keytool -import -noprompt -file '+importKeystorePath+importCertName+' -keystore '+ keyPath+' -alias '+aliasName+' -storepass ' +storePass

            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=serverName,port=22,username=userName,password=password)

            stdin,stdout,stderr=ssh.exec_command(importCommand)

            outlines=stdout.readlines()
            Output=''.join(outlines)
            ssh.close()
            return {"Status":"Success",'Output':json.dumps(Output)}
        except Exception as e:
            return {'Exception' : str(e)}
 

if __name__ == "__main__":
    context = {}
    
    bot_obj = RenewCertificate()
    
    '''context = {"serverName":"10.138.13.46","userName":"admin","password":"April@2020",
               "importKeystorePath":"/Nia/ambaridata/configuration/tomcat_cas/",
               "importCertName":"niatomcat_test.crt",
               "keyPath":"/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.201.b09-2.el7_6.x86_64/jre/lib/security/cacerts",
               "aliasName":"niajo_test",
               "storePass":"changeit"} '''
    context = {"serverName":"",
               "userName":"",
               "password":"",
               "importKeystorePath":"",
               "importCertName":"",
               "keyPath":"",
               "aliasName":"",
               "storePass":""}
    
    bot_obj.bot_init()
    #Calling of execute function on linux server
    output = bot_obj.execute(context)
    print(output)  
