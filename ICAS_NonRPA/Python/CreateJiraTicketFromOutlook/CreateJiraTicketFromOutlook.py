'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import re
from jira import JIRA
from ast import literal_eval
from abstract_bot import Bot

# Python Bot to create JIRA issue

##################################################
## From the email body , using regex we will fetch 
## subject, body, project key and description of ticket.
##################################################

class CreateJiraTicketFromOutlook(Bot):

    def execute(self, executeContext) :
        try:
            jiraServer = executeContext['jiraServer']
            if  not jiraServer:
                return {'validation error' : 'missing argument jiraServer'}

            jiraUsername = executeContext['jiraUsername']
            if  not jiraUsername:
                return {'validation error' : 'missing argument jiraUsername'}

            jiraPassword = executeContext['jiraPassword']
            if  not jiraPassword:
                return {'validation error' : 'missing argument jiraPassword'}

            emailData = executeContext['emailData']
            if  not emailData:
                return {'validation error' : 'missing argument emailData'}

            username = jiraUsername
            password = jiraPassword
            jira = JIRA(basic_auth=(username, password), 
                            options = {'server': jiraServer})
            print ("connection done")
            emailData = executeContext['emailData']
            emailData = literal_eval(emailData) 

            jiraProject = ''
            project_key = ''
            description = ''
            for i in emailData:
                print ("=========================================")
                sender_name = i['Sender']
                subject = i['Subject'].lower()
                if 'ticket' in subject or 'jira' in subject:
                    if 'jira' in i['Body'].lower():
                        projectSearch = re.search('(?<=key )(\w+)', i['Body'])       # fetching next word i.e. project_key name after word 'key' in body
                        if projectSearch:
                            project_key =  projectSearch.group(1)
                        
                        descriptionSearch = re.findall(r"'(.*?)'", i['Body'])            # fetching last single-quotes enclosed value i.e description from email body
                        if descriptionSearch:
                            description = descriptionSearch[-1]

                        if project_key and description:
                            issue_dict = {
                                'project': {'key': project_key},                                       # key or ID of project can be passed
                                'summary': description,
                                'issuetype': {'name': 'Bug'},
                    
                            }
                            try:
                                new_issue = jira.create_issue(fields=issue_dict)
                                print  ("Issue created in JIRA")
                            except Exception as e:
                                print('Exception : ',str(e))
                        else:
                            print (" Info : 'Subject' or 'description' of issue not found")
                    else:
                        print ("Info  :  Email Body is without keywords 'JIRA' ")
                else:
                    print ("Info  :  Email subject is without keywords 'JIRA' or 'Ticket'")
            print ("=========================================")
            print ("All emails processed")
            return {'status': 'success'}
        except Exception as e:
            return {'Exception': str(e)}

       
        
if __name__ == '__main__':
    context = {}
    bot_obj = CreateJiraTicketFromOutlook()

    context = {
                'jiraServer': '',
                'jiraUsername': '',
                'jiraPassword': '',
                'emailData ' : '',

                # 'jiraServer': 'https://infosysjira.ad.infosys.com/',
                # 'jiraUsername': 'username',
                # 'jiraPassword': 'password',
                # 'emailData' : '[{"Sender": "User1", "Subject": "Create ticket in JIRA", "Body": "Hello,create ticket in JIRA on project key IMGD  with description \'DELETE THIS ! TESTING ONLY\'."}, {"Sender": "User 2", "Subject": "Create Email", "Body": "Hello,create ticket in JIRA on project key IMGD  with description \'DELETE THIS ! TESTING ONLY\'."}]'
                
              
            }
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print('output : ',output)