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

# -- bot for fetching file names from given directory and for sorting the names --
class GettingMailDetailUsingID(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):
        mail_id = executionContext['mail_id']
        try:
            # create outlook object
            outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
            ls = outlook.GetItemFromId(mail_id)
            body = ls.Body

            
            return {'mail_body':body}
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          return {'Error' : formatted_lines[-1]} 

if __name__ == "__main__":
    context = {}
    bot_obj = GettingMailDetailUsingID()

    context = {'mail_id':'00000000933855E2BCD1C24694B80A1C23FCAA470700432B95F531F5F24A913CC4A28750FE9400012DC030AF0000432B95F531F5F24A913CC4A28750FE9400012DC04FD70000'}

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)