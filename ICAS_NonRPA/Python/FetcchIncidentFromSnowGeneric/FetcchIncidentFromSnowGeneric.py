'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
#<pysnow.client.Client object at 0x0000024FF1BF1780>
##Fetch incident details from serviceNow
#!/usr/bin/python

from abstract_bot import Bot
import pysnow
import pandas as pd
import json

class FetcchIncidentFromSnowGeneric(Bot):

    def bot_init(self):
        pass


    def execute(self, executeContext):
        try:
            instance = executeContext['instance']
            user = executeContext['user']
            password = executeContext['password']
            Query = executeContext['Query']
           
            dataframe = pd.DataFrame(columns=['incident_id']) 
            conn = pysnow.Client(instance=instance, user=user, password=password)
            
			
			#  using the incident table API
            incident = conn.resource(api_path='/table/incident')
			# Query for incidents with category is ORC
            response = incident.get(query = Query)
            print(type(Query))
            print(Query)
            print(response)
			
			# Iterate over the result and print out `short_description` of the matching records.
            for incidents in response.all():
                dataframe = dataframe.append({'incident_id':incidents['number']},ignore_index=True)            
                
                
            js = dataframe.to_json(orient='records')
            
            return {'Incident_Table':json.loads(js)}

        except Exception as e:
            print("error")
            return {'Exception':str(e)}

if __name__ == '__main__':
    context = {}
    output = {}
    obj_snow = FetcchIncidentFromSnowGeneric()

    #context = {'instance' : "dev62689",'user' : "admin",'password' : "Infy@1234","Query":{'category':"ORC"}}
    context = {'instance' : "",'user' : "",'password' : "", "Query":''}
	#context={'conn' : "conn"}
    # print(dir(obj_snow))
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
    # output=['INC0010055 : Order 1110001 is type of cancel order','INC0010056:order 1110002 is type of  place hold', 'INC0010057:order 1110003 is for type Stop manufacturing', 'INC0010058:order 1110004 is type of  changed date']}
    