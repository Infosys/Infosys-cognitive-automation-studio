'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 17:41:19 2020

@author: anuj.gupta03
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 19:19:25 2020

@author: anuj.gupta03
"""

import os
import subprocess
import shutil
from abstract_bot import Bot

# Bot to check CPU usage(utilizations) and alert
class StartServer(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        try:    
            var_directory_name=executionContext['var_directory_name']
            process_name=executionContext['process_name']
            
            
            
            if var_directory_name is None:
                return ("Missing Arguments: Directory Name")
            if process_name is None:
                return ("Missing Arguments: process Name")
            
            
            if process_name == "start":
                os.getcwd()
                os.chdir(r""+var_directory_name)
                os.getcwd()
                subprocess.call('startup',shell=True)
                #subprocess.call('catalina.sh start',shell=True)
                print ("Tomcat started successfully")
                Output={'status':'Tomcat started successfully','status_code':'1'}
            elif process_name == "stop":
                os.getcwd()
                os.chdir(r""+var_directory_name)
                os.getcwd()
                #subprocess.call('catalina.sh stop',shell=True)
                os.system('catalina.sh stop')
                print ("Tomcat stopped successfully")
                Output={'status':'Tomcat stopped successfully','status_code':'2'}
            elif process_name == "restart":
                os.getcwd()
                os.chdir(r""+var_directory_name)
                os.getcwd()
                subprocess.call('catalina.sh stop',shell=True)
                subprocess.call('catalina.sh startup',shell=True)
                print ("tomcat restarted successfully")
                Output={'status':'Tomcat restarted successfully','status_code':'3'}
            
            return Output
            
        except Exception as e:
            return {'Exception' : str(e),'status_code':'0'}
        
            
if __name__ == "__main__":
    context = {}
    bot_obj = StartServer()
    context={'var_directory_name':'','process_name':''}
    #Variable to be passed as argument
    #give server name as IP only
    #context = {'var_directory_name':'C:\\Users\\anuj.gupta03\\Downloads\\apache-tomcat-9.0.10\\apache-tomcat-9.0.10\\bin','process_name':'start'}
               

   
    output = bot_obj.execute(context)
    print(output)  
    
    
    
    
    #else:
                #Output={'status':'Give right process Name'}