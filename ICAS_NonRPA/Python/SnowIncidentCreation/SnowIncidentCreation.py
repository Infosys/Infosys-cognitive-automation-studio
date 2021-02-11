'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import win32com.client
import pysnow
import traceback
import sys
import json

from abstract_bot import Bot

# -- bot for fetching file names from given directory and for sorting the names --
class SnowIncidentCreation(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):
       # Itsm_Tool = executionContext['Itsm_Tool']
        instance_id = executionContext['instance_id']
        user_name = executionContext['user_name']
        password = executionContext['password']
        mail_body=executionContext['mailbody']
        assignment_group = executionContext['assignment_group']
        assigned_to = executionContext['assigned_to']

        
        try:
            c = pysnow.Client(instance=instance_id, user=user_name, password=password)
            # Define a resource, here we'll use the incident table API 
            incident = c.resource(api_path='/table/incident')
            # Set the payload 
            new_record = { 'short_description': 'New BotFactory ticket', 'description': mail_body,'assignment_group':assignment_group,'assigned_to':assigned_to}
            # Create a new incident record 
            result = incident.create(payload=new_record)
                        #print(result)
            #return {'output':json.loads(str(result._response.content))}
			return {"output":result}
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Error' : formatted_lines[-1]} 

           

if __name__ == "__main__":
    context = {}
    bot_obj = SnowIncidentCreation()

    #context = {'instance_id':'dev95176','user_name':'admin','password':'hx08NdTBnlXW','mailbody':'HERSHEY_Logical Disk Free Space is low * The disk D: on computer dcsbl81tst01.hersheys.com is running out of disk space. The values that exceeded the thresho','assignment_group':4 }
    context = {'instance_id':'','user_name':'','password':'','mailbody':'','assignment_group':'','assigned_to':'' }
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)