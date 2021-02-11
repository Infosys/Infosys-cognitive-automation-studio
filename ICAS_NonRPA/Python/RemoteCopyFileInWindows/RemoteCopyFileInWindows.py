'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import os
import shutil
import win32wnet

class RemoteCopyFileInWindows(Bot):

    def bot_init(self):
        pass
            
    def covert_unc(self,host, path):
#    Convert a file path on a host to a UNC path.
        print(host)
        return ''.join(['\\\\', host, '\\', path.replace(':', '$')])

    def wnet_connect(self,host, username, password):
        unc = ''.join(['\\\\', host])
        print(unc,username,password)
        try:
            print("hhhiiiiihh")
            win32wnet.WNetAddConnection2(0, None, unc, None, username, password)
            print("hhhhh")
        except Exception as err:
            print(err)
            if isinstance(err, win32wnet.error):
                print(err[0])
            # Disconnect previous connections if detected, and reconnect.
                if err[0] == 1219:
                    win32wnet.WNetCancelConnection2(unc, 0, 0)
                    return self.wnet_connect(host, username, password)
                raise err
   
        
    def execute(self, executeContext):
      
            serverName = executeContext['serverName']
            userName = executeContext['userName']
            password = executeContext['password']
            localFilePath = executeContext['localFilePath']
            remoteFilePath = executeContext['remoteFilePath']
            try:
#                deployStatus = self.netcopy(serverName,userName,password,localFilePath,remoteFilePath)
                 self.wnet_connect(serverName, userName, password)
                 print("here")
                 remoteFilePath = self.covert_unc(serverName, remoteFilePath)
                 print(remoteFilePath)
                 if os.path.isdir(localFilePath):
                     shutil.copytree(localFilePath, remoteFilePath)
                     return {'Output':'Copied the folder Sucessfully'}
                 elif os.path.isfile(localFilePath):
                     shutil.copy(localFilePath, remoteFilePath)
                     return {'Output':'Copied the file Sucessfully'}
                 else:
                     print('%s is neither a file nor directory' % (localFilePath))
    
            except Exception as e:
                return {'Exception':str(e)}
   

if __name__ == '__main__':

    context = {}
    bot_obj = RemoteCopyFileInWindows()
    #context = {'serverName' :'vimppnz02-01','userName':'itlinfosys\harika.todupunoori','password':'','localFilePath':'c:/users/harika.todupunoori/desktop/apple.bat','remoteFilePath':'c:/users/harika.todupunoori/desktop/apple.bat'}
    context = {'serverName' :'','userName':'','password':'','localFilePath':'','remoteFilePath':''} 
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
