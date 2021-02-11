'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import json
import traceback
import sys
import win32com.client
import pysnow
import pandas as pd
from abstract_bot import Bot

# -- bot for fetching file names from given directory and for sorting the names --
class RetrieveUnreadMailDetails(Bot) :


    def bot_init(self):
        pass

    def execute(self, executionContext):

        folder_name = executionContext['folder_name']
        try:
            # create outlook object
            outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
            dataframe = pd.DataFrame(columns=['Id','Subject','Importance','Unread','From'])
            root_folder = outlook.Folders.Item(1)
            folder_list= root_folder.Folders
            folder_name_list=[]
            subFolder_list=[]
            subFolder_name_list=[]
            for folder in folder_list:
                folder_name_list.append(folder.name)
                subFolder_list.append(folder.Folders)
            
            
            if(folder_name in folder_name_list):
                for folder in folder_list:
                    if(folder.Name== folder_name):
                        contents = folder.Items
                        for content in contents:
                            if(content.Unread == True):
                                dataframe = dataframe.append({'Id':content.EntryID,'Subject':content.Subject,'Importance':content.Importance,'Unread':content.Unread,
                                                     'From':content.Sender},ignore_index=True)
                                content.Unread = False
                            else:
                                pass
                             #print("No Unread Messages")
            else:
                # inbox = outlook.GetDefaultFolder(6)
                # folders = inbox.Folders
                for subfolder in subFolder_list:
                    for subFolder_name in subfolder:
                        subFolder_name_list.append(subFolder_name.name)
                if(folder_name in subFolder_name_list):
                    for subfolders in subFolder_list:
                        for folder in subfolders:
                            if(folder.Name== folder_name):
                                contents = folder.Items
                                for content in contents:
                                    if(content.Unread == True):
                                        dataframe = dataframe.append({'Id':content.EntryID,'Subject':content.Subject,'Importance':content.Importance,'Unread':content.Unread,
                                                     'From':content.Sender},ignore_index=True)
                                        content.Unread = False
                                    else:
                                        pass
                            #print("No Unread Messages")
                            else:
                                pass
            
            
            js = dataframe.to_json(orient='records')
            return {'Mails':json.loads(js)}
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          return {'Error' : formatted_lines[-1]} 

if __name__ == "__main__":
    context = {}
    bot_obj = RetrieveUnreadMailDetails()

    context = {'folder_name':'Junk Email'}

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)