'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import pysnow
import json

class UpdateSnow(Bot):

    def bot_init(self):
        pass


    def execute(self, executeContext):
        instance1 = executeContext['instance']
        user1 = executeContext['user']
        password1 = executeContext['password']
        incidentno = executeContext['inc_no']
        inc_state = executeContext['inc_state']
        
        #work_order_item = executeContext['workrder_id']

        try:
            c = pysnow.Client(instance= instance1, user=user1 , password=password1)
        
           
            # Define a resource, here we'll use the incident table API
            incident = c.resource(api_path='/table/incident')

            # Query for incidents with state 3
            #update = {'short_description': 'hello' }
            update = {'incident_state': inc_state ,'close_code': 'Solved (Work Around)','close_notes': 'hello'}
            # Update 'short_description' and 'state' for 'INC012345'
            updated_record = incident.update(query={'number': incidentno}, payload=update)
            
                    
            return{'Updated_record': updated_record.all()}
           
        except Exception as e:
            #print("error")
            return {'Exception':str(e)}

if __name__ == '__main__':
    context = {}
    obj_snow = UpdateSnow()

    context = {'instance' : "", "user" : "", "password" : "", 'inc_no':'',"inc_state":""}
    #context = {'instance' : "dev62689", "user" : "admin", "password" : "Infy@1234",'inc_no': "INC0010044","inc_state":"6"}
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
    
    #INC0010021