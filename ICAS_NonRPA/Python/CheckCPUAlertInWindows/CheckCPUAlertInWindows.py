'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:23:24 2020

@author: anuj.gupta03
"""

import wmi
from socket import *
from abstract_bot import Bot

# Bot to check CPU usage(utilizations) and alert
class CheckCPUAlertInWindows(Bot):
    
    def bot_init(self):
        pass
    
    def  execute(self,executionContext):
        virtualMachineIp=executionContext['virtualMachineIp']
        userName = executionContext['userName']
        password = executionContext['password']
        thresholdValue=executionContext['thresholdValue']
        
        try:
            #print('Establishing connection to {0}'.format(virtualMachineIp))
            #print('userName: {0}'.format(userName))
            
            #for remote connection=======================
            connection = wmi.WMI(virtualMachineIp, user= userName,password= password)
            
            #for local system============================
            #connection=wmi.WMI()
            print('Connection established')

            utilizations = [cpu.LoadPercentage for cpu in connection.Win32_Processor()]
            utilization = int(sum(utilizations) / len(utilizations))
            
            if utilization < int(thresholdValue):
                print("CPU is in good condition")
            else:
                print("CPU Overloaded. Close some connection")

            
            cpu_usage=utilization
            output= {'CpuUsageInPercentages': cpu_usage}
            return output            
        
        except Exception as e:
               print('Your userName and Password of '+getfqdn(virtualMachineIp)+' are wrong.')
               return {'Exception' : str(e)}
               
           
if __name__ == "__main__":
    context = {}
    bot_obj=CheckCPUAlertInWindows()
    
    context={'virtualMachineIp':'',
             'userName':'',
             'password':'',
             'thresholdValue':''}

    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)
        

        
