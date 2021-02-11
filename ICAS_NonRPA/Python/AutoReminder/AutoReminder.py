'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:01:47 2020

@author: anuj.gupta03
"""

#from abstract_bot import Bot

import pysnow
from abstract_bot import Bot
from datetime import date,timedelta,datetime

class AutoReminder(Bot):
    
    def bot_init(self):
        pass
    
    def execute(self, executeContext):
        try:
            instance = executeContext['instance']
            user = executeContext['user']
            password = executeContext['password']            
            incidentId=executeContext['incidentId']
            no_of_days=executeContext['no_of_days']    
            
            conn = pysnow.Client(instance=instance, user=user, password=password)
            qb = (pysnow.QueryBuilder().field('state').equals('1'))
                                       
            #  using the incident table API
            incident = conn.resource(api_path='/table/incident')

            result = incident.get(query=qb,stream=True)           

            
            
            today=date.today()
            
            #for a particular incident id
            for record in result.all():
                if record['number']==incidentId:               
                    ticket_opened_date = datetime.strptime(record['opened_at'], '%Y-%m-%d %H:%M:%S').date()
                    #no_of_days is for how many days ticket will be considered as valid
                    no_of_dayss=int(no_of_days)
                    
                    ticket_validity_date=ticket_opened_date+timedelta(no_of_dayss)
                    
                    aging_of_ticket=today-ticket_validity_date
                    
                        
        
            
            return{'Aged Ticket':str(aging_of_ticket)}
            #for a particular user all the open incident
            """
            info = []
            for record in result.all():
                ticket_opened_date = datetime.strptime(record['opened_at'], '%Y-%m-%d %H:%M:%S').date()
                    
                no_of_dayss=int(no_of_days)
                    
                ticket_validity_date=ticket_opened_date+timedelta(no_of_dayss)
                    
                aging_of_ticket=today-ticket_validity_date
                    
                info.append({"incidentId":record['number'],"aging_of_ticket":aging_of_ticket})
            return{'incident_List': json.dumps(info)}"""

 

        except Exception as e:

            print("error")

            return {'Exception':str(e)}

 

if __name__ == '__main__':

    context = {}

    bot_obj = AutoReminder()   

    #context = {'instance' : 'dev82133','user' : 'admin','password' : 'Zainu01$$','incidentId':'INC0010005','no_of_days':'3'}
    context = {'instance' : '','user' : '','password' : '','incidentId':'','no_of_days':''}

 

    bot_obj.bot_init()

    output = bot_obj.execute(context)

    print(output)