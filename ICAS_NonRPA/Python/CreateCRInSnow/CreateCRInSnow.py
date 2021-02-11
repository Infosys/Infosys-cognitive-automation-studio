'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pysnow
import traceback
import sys
from abstract_bot import Bot

# -- bot for fetching file names from given directory and for sorting the names --
class CreateCRInSnow(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):
        instanceId = executionContext['instanceId']
        userName = executionContext['userName']
        password = executionContext['password']
        description=executionContext['description']
        assignmentGroup = executionContext['assignmentGroup']
        assignedTo = executionContext['assignedTo']

        
        try:
            c = pysnow.Client(instance=instanceId, user=userName, password=password)
           
            new_record = { 'short_description': 'New BotFactory ticket', 'description': description,'assignment_group':assignmentGroup,'assigned_to':assignedTo}
             # Set the payload 
            result = c.insert(table="change_request", payload=new_record)
#            print("The created incident is : ",result.get("number"))
            return {'output': "Success : created with Id "+result.get("number")}

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Exception' : formatted_lines[-1]} 

           

if __name__ == "__main__":
    context = {}
    bot_obj = CreateCRInSnow()
#    context = {'instanceId':'dev82133','userName':'admin','password':'','description':'testing','assignmentGroup':'Database','assignedTo':'David Dan'}
    context = {'instanceId':'','userName':'','password':'','description':'','assignmentGroup':'','assignedTo':''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
