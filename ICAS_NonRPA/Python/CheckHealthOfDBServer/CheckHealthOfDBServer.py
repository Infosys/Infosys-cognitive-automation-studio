'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#dependency to be installed before running 
#pip install paramiko run this command to install dependency
import paramiko
import sys
import traceback
import mysql.connector
from mysql.connector import Error

from abstract_bot import Bot
#bot to connect to linux server
class CheckHealthOfDBServer(Bot):
    
    def bot_init(self):
        pass
        
    def execute(self,executionContext):
        try:
            hostName =executionContext["hostName"]
            port =executionContext["port"]
            userName=executionContext["userName"]
            password=executionContext["password"]
            #condition to check values
            if hostName is None:
                return ("Missing argument : hostName")
            if port is None:
                return ("Missing argument : port")
            if userName is None:
                return ("Missing argument : userName")
            if password is None:
                return ("Missing argument :password")

            #connecting to server
            connection = None
            connection = mysql.connector.connect( host=hostName,port=port, user=userName, passwd=password)
            print("Connection to MySQL DB successful")
            return {'Output':"Connection to MySQL DB successful"}
    
        except Error as e:
            print(f"The error '{e}' occurred")
            return {'Exception' : "The error '{e}' Occured"} 


if __name__ == "__main__":
    context = {}
    bot_obj = CheckHealthOfDBServer()
    #variable to be passed as parameter
    context = {'hostName':'','port':'3306','userName':'','password':''}
    #function calling to connect to linux server and return object
    bot_obj.bot_init()
    output = bot_obj.execute(context)