'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

from abstract_bot import Bot
import ldap

class AddUserRoleInLDAP(Bot):
    def bot_init(self):
        pass
    
    def execute(self, executeContext):
        try:
            serverIP=executeContext['serverIP']
            portNumber=executeContext['portNumber']
            
            dnAuth=executeContext['dnAuth']
            password=executeContext['password']
            
            dnMod=executeContext['dnMod']
            newRole=executeContext['newRole']
            
            action=executeContext['action']
            
            if serverIP=="":
                return{'Missing Argument':'serverIP'}
            if portNumber=="":
                return{'Missing Argument':'portNumber'}
            if dnAuth=="":
                return{'Missing Argument':'dnAuth'}
            if password=="":
                return{'Missing Argument':'password'}
            if dnMod=="":
                return{'Missing Argument':'dnMod'}
            if newRole=="":
                return{'Missing Argument':'newRole'}
            if action=="":
                return{'Missing Argument':'action'}

            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT,0)
            l = ldap.initialize("ldaps://"+serverIP+":"+portNumber)   #serverIP and portNumber for connecting to the server
            l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
            l.set_option(ldap.OPT_NETWORK_TIMEOUT, 10.0)
            l.simple_bind_s( dnAuth, password ) #Bind/authenticate with a user with apropriate rights to add/modify roles
            
            #Adding the role of user.
            if action.lower=='add':
                modAttrs = [( ldap.MOD_ADD, 'role', newRole )] #modifying the 'role' atrribute present in the user's attributes.
                l.modify_s(dnMod, modAttrs)
                return{'output':'Successfully added the role for the given user'}
            
            #Modifying the role of the user
            elif action.lower=='modify':
                modAttrs1 = [( ldap.MOD_REPLACE, 'role', newRole )]
                l.modify_s(dnMod, modAttrs1)
                return{'output':'Successfully modified the role for the given user'}
    
        except Exception as e:
            return{'Exception':str(e)}
        
if __name__ == '__main__':
    context = {}
    obj = AddUserRoleInLDAP()
    context = {
            'serverIP':'',      #serverIP of the ldap server to connect to
            'portNumber':'',    #portNumber of the ldap server to connect to
            'dnAuth':'',  	    #dn of the user authorized to add/modify roles
            'password':'',	    #password of the user authorized to add/modify roles
            'dnMod':'',	        #dn of the user whose role needs to added/modified
            'newRole':'',		#new role for the user
            'action':''			#action could be either: 'ADD' or 'MODIFY'
                }
    '''  
    #Sample Data for input variables          
    context = {
            'serverIP':'10.99.0.214',   #serverIP of the ldap server to connect to
            'portNumber':'636',			#portNumber of the ldap server to connect to
            'dnAuth':'uid=matt,ou=users,dc=example,dc=com',  	#dn of the user authorized to add/modify roles
            'password':'secret',							 	#password of the user authorized to add/modify roles
            'dnMod':'uid=francis,ou=users,dc=example,dc=com',	#dn of the user whose role needs to added/modified
            'newRole':'ADMIN',			#new role for the user
            'action':'ADD'				#action could be either: 'ADD' or 'MODIFY'
                }
    '''
    obj.bot_init()
    output = obj.execute(context)
    print(output)
            
