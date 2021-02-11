'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
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
class DeployFile(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self,executionContext):
        try:    
            var_directory_name=executionContext['var_directory_name']
            var_source=executionContext['var_source']
            var_destination=executionContext['var_destination']
            
            
            if var_directory_name is None:
                return ("Missing Arguments: Directory Name")
            if var_source is None:
                return ("Missing Arguments: source location")
            if var_destination is None:
                return ("Missing Arguments: Destination location")
            
            shutil.copy(var_source, var_destination)
            
            os.getcwd()
            os.chdir(r""+var_directory_name)
            os.getcwd()
            subprocess.call('catalina.sh stop',shell=True)
            subprocess.call('startup',shell=True)
            print ("tomcat started successfully and file deployed successfully")
            Output= {'status':'ok'}
            return Output
            
        except Exception as e:
            return {'Exception' : str(e)}
        
            
if __name__ == "__main__":
    context = {}
    bot_obj = DeployFile()
    context={'var_directory_name':'','var_source':'','var_destination':''}
            
    #Variable to be passed as argument
    #give server name as IP only
    #context = {'var_directory_name':'C:\\Users\\anuj.gupta03\\Downloads\\apache-tomcat-9.0.10\\apache-tomcat-9.0.10\\bin',
               #'var_source':'C:\\Users\\anuj.gupta03\\New folder\\try13.war',
               #'var_destination':'C:\\Users\\anuj.gupta03\\Downloads\\apache-tomcat-9.0.10\\apache-tomcat-9.0.10\\webapps' 
               #}
               

   
    output = bot_obj.execute(context)
    print(output)  
    
    
    
    
    