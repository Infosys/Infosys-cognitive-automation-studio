'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
from socket import *
import win32api
import win32net
import random
import string
import sys
import traceback
from abstract_bot import Bot

class CheckFailureOfDBJobs(Bot):
    
    def bot_init(self):
        pass
        
    def execute(self,executionContext):
        
        def get_DriveLetter():
            drives= win32api.GetLogicalDriveStrings()
            Current_Drives= [x[0] for x in drives.split("\000")[:-1]]
            
            for letter in string.ascii_letters[26:]:
                if letter not in "".join(Current_Drives):
                    return letter
        try:  
            ipAddress =executionContext["ipAddress"]
            userName=executionContext["userName"]
            password=executionContext["password"]
            remoteFolder= executionContext["remoteFolder"]
            remoteFileName= executionContext["remoteFileName"]
            logOutputFile= executionContext["logOutputFile"]
            
                #condition to check values
            if ipAddress is None:
                return ("Missing argument : ipAddress")
            if userName is None:
                return ("Missing argument : userName")
            if  password is None:
                return ("Missing argument :password")
            if  remoteFolder is None:
                return ("Missing argument :remoteFolder")
            if  remoteFileName is None:
                return ("Missing argument :remoteFileName")
            if  logOutputFile is None:
                return ("Missing argument :logOutputFile")
            
            use_dict={}
            use_dict['password']=str(password)
            use_dict['username']=str(userName)
            use_dict['remote'] = remoteFolder 
            use_dict['local'] = get_DriveLetter()+":"
            win32net.NetUseAdd(None, 2, use_dict)
   
            f = open((use_dict['local']+'\\'+remoteFileName), "r")
            with open(logOutputFile, 'a',encoding= "utf-8") as file:
                for line in f:
                    if ("Event Scheduler" in line) and "ERROR" in line:
                        file.write(line)
                file.close()
                        
            return {'Output':'Log File Accessed'}
    
        except Exception as e:
            return {'Exception' : str(e)} 
    

if __name__ == "__main__":
    context = {}
    bot_obj = CheckFailureOfDBJobs()
    #variable to be passed as parameter
    context = {'ipAddress':'','userName':'','password':'','remoteFolder':'','remoteFileName':'mysql.log','logOutputFile': ''}
    #function calling to connect to linux server and return object
    bot_obj.bot_init()
    bot_obj.execute(context)
