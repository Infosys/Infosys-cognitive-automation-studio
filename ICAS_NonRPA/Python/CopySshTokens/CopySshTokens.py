'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import paramiko
import time
from abstract_bot import Bot


class CopySshTokens(Bot):
    
    def bot_init(self):
        pass
   
    def execute(self,executionContext):
        try:
            serverName =executionContext['serverName']
            userName=executionContext['userName']
            password=executionContext['password']
            remoteServerName=executionContext['remoteServerName']
            remoteUserName=executionContext['remoteUserName']
            remoteServerPassword=executionContext['remoteServerPassword']


            # connecting to server
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=serverName,port=22,username=userName,password=password)
            print('Successfully connected to %s' % serverName)
            remote_conn = ssh.invoke_shell()
            output = remote_conn.recv(1000)
            
            remote_conn.send(f'ssh-copy-id -i ~/.ssh/id_rsa {remoteUserName}@{remoteServerName}\n')
            time.sleep(2)
            
            if remote_conn.recv_ready():
                output = remote_conn.recv(1000)
                print(output)
            
            remote_conn.send(f'{remoteServerPassword}\n')
            time.sleep(2)
            
            if remote_conn.recv_ready():
                Output = remote_conn.recv(5000)
            print(Output)
            
            ssh.close()
            return {'Output':'Success'}
        except Exception as e:
            return {'Exception' : str(e)}
 

if __name__ == "__main__": 
    context = {}
    
    bot_obj = CopySshTokens()
    
    ''' context = {'serverName':"10.138.13.46",'userName':"admin",'password':"April@2020",
               'remoteServerName':'10.138.13.39','remoteServerPassword':'April@2020',
               'remoteUserName':'admin'} '''
    
    context = {'serverName':"",'userName':"",'password':"",
               'remoteServerName':'','remoteServerPassword':'',
               'remoteUserName':''}
    
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)  
