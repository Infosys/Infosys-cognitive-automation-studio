'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 11:39:11 2020

@author: Shravanthi_B01
"""

# import the win32com library
import win32com.client
from win32com.client import Dispatch
from abstract_bot import Bot

class DownloadOutlookEmailAttachment(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):
        try:
            path = executeContext['file_storage_path']

            namespace = Dispatch("Outlook.Application").GetNamespace("MAPI").Session
            print (namespace)

            inboxfolder = namespace.GetDefaultFolder("6")
        # get messages on Inbox folder
            messages = inboxfolder.Items

            print ("=====Fetching all items in Inbox======")
        
        # get message contents
            attachment_name = ''
        
            for message in messages:
                if message.UnRead == True:
                    print("Unread email",message.Attachments)
                    for attachments in message.Attachments:                    
                    #Saves to the attachment to the working directory 
                        attachment = message.Attachments.Item(1)
                        attachment_name = str(attachment)
                        attachment.SaveASFile(path + str(attachment))
                        print("inside second for loog")
                        message.Unread = False
                        return {"attachment":path + attachment_name}
                    break
            if attachment_name:
                return {'output': '{0}{1}'.format(path + attachment_name)}
            else:
                return {'output': 'no attachment found'}
        except Exception as e:
            return{'Exception': str(e)}        
    
if __name__ == '__main__':
    context = {}
    output = {}
    obj_snow = DownloadOutlookEmailAttachment()
    context = {
            #'file_storage_path' : ''
            'file_storage_path' : ""
                }
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)