'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import traceback
import sys
import win32com.client
import pysnow
import pandas as pd
from abstract_bot import Bot
import json

# -- bot for fetching file names from given directory and for sorting the names --
class FetchFirstIncidentSnow(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):
        inc_no = executionContext['inc_no']
        instance = executionContext['instance']
        user = executionContext['user']
        password = executionContext['password']
        try:
            # Connect with Service Now
            conn = pysnow.Client(instance=instance, user=user, password=password)
            incident_details = conn.resource(api_path='/table/incident').get(query={'number':inc_no})
            #print(incident_details.all())
            
            return {"short_desc": incident_details['short_description'],"work_order_number":incident_details['u_workorderno'],"status":incident_details['incident_state'],"order_number":incident_details['u_orderno']}
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          return {'Error' : formatted_lines[-1]} 

if __name__ == "__main__":
    context = {}
    bot_obj = FetchFirstIncidentSnow()

    #context = {'inc_no':'INC0010061 ','instance' : "dev62689",'user' : "admin",'password' : "Infy@1234"}
    context = {'inc_no':'','instance' : "",'user' : "",'password' : ""}

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)