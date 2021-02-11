'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import pysnow
import json

class UpdateSnowGeneric(Bot):

    def bot_init(self):
        pass


    def execute(self, executeContext):
        instance1 = executeContext['instance']
        user1 = executeContext['user']
        password1 = executeContext['password']
        incidentno = executeContext['inc_no']
        update_query = executeContext['update_query']
        
        #work_order_item = executeContext['workrder_id']

        try:
            c = pysnow.Client(instance= instance1, user=user1 , password=password1)
        
           
            # Define a resource, here we'll use the incident table API
            incident = c.resource(api_path='/table/incident')

            # Query for incidents with state 3
            #update = {'short_description': 'hello' }
            update = update_query
            # Update 'short_description' and 'state' for 'INC012345'
            updated_record = incident.update(query={'number': incidentno}, payload=update)
            
                    
            return{'Updated_record': updated_record.all()}
           
        except Exception as e:
            #print("error")
            return {'Exception':str(e)}

if __name__ == '__main__':
    context = {}
    obj_snow = UpdateSnowGeneric()

    
    context = {'instance' : "dev74082", "user" : "admin", "password" :"Servicenow@123",
    "update_query":{'incident_state': "6" ,'close_code': 'Solved (Work Around)','close_notes': 'hello'},
    "inc_no":"INC0010012"}
    #context = {'instance' : "", "user" : "", "password" : "",
    #"update_query":{'incident_state': "" ,'close_code': '','close_notes': ''},
    #"inc_no":""}


    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
    
    #INC0010021