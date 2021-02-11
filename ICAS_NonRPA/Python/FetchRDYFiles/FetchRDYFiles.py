'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import math
import json
import datetime
from datetime import datetime
from abstract_bot import Bot
from os import listdir
from os.path import isfile, join


# Python bot to find .rdy files from a given location
# Name of the file must begin with ropin
# ex. ropinf.190614.160103.rdy

class FetchRDYFiles(Bot):

    def bot_init(self):
        pass
  
    def execute(self, executeContext) :
        try:
            
            mypath=executeContext['filepath']
            files_available = [f for f in listdir(mypath) if isfile(join(mypath, f))]
            
            # storing all .rdy files in an array
            list_rdy = []
            for files in files_available:
                if((".rdy" in files) & ("ropin" in files)):
                    list_rdy.append(files)
            print(list_rdy)


            file_received_today = 0
            file_received_today_after_5 = 0
            no_file_received_today = 0
            
            
            
            # if NO .rdy files are found
            if len(list_rdy) == 0:
                print ('NO .rdy files ')
                return  {'mail_status_code' : '1' }
           
            # validating file with today's date and 5:00 AM time
            for files in list_rdy:
                n=2
                if(len(files.split('.')) >=4):
                    date1 = files.split('.')[1]
                    time1 = files.split('.')[2]
                    date2 = '/'.join([date1[i:i+n] for i in range(0, len(date1), n)])
                    time2 = ':'.join([time1[i:i+n] for i in range(0, len(time1), n)])
                    timestamp = date2 +' '+ time2
                    
                    converted_datetime= datetime.strptime(timestamp, '%y/%m/%d %H:%M:%S')
                    
                    if (converted_datetime.day == int(datetime.today().strftime("%d")) and converted_datetime.month == int(datetime.today().strftime("%m"))
                        and converted_datetime.year == int(datetime.today().strftime("%Y"))):       # if file is received today
                        file_received_today = file_received_today + 1
                        if (converted_datetime.hour <= 5):                                     # if file is received today before 5
                            print ('File received BEFORE 5')                                     
                            filename = '{0}/{1}'.format(mypath,files)
                            return  {'mail_status_code' : '0' , 'filename' : filename}         # returns name of file, and No mail will be send
                        elif (converted_datetime.hour > 5):                                    # if file is received later then 5
                            print ('File received AFTER 5')
                            file_received_today_after_5 = file_received_today_after_5 + 1
                           
                    else:
                        no_file_received_today = 0

            if file_received_today_after_5 > 0:
                return  {'mail_status_code' : '2' }                     # mail for file received after 5 AM
            if file_received_today > 0:
                return  {'mail_status_code' : '0' }                     # No mail will be send
            return  {'mail_status_code' : '1' }                         # mail for file not found
            
        except Exception as e:
            print("Error occured",str(e)) 
            return {'status' : str(e) }

  
if __name__ == '__main__':
    context = {}
    bot_obj = FetchRDYFiles()

    context = {
                'filepath':''   
}

    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)