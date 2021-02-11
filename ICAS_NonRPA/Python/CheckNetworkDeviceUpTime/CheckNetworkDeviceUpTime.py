'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from abstract_bot import Bot
import netmiko

#Python Bot will check the Network Uptimes and save them in a CSV file 
class CheckNetworkDeviceUpTime(Bot):
    def bot_init(self):
        pass
    def execute(self,executionContext):
        userName=executionContext["userName"]
        passWord=executionContext["passWord"]
        filePath=executionContext["filePath"]
        deLimiter=executionContext["deLimiter"]
        if userName is None:
            return ("Missing argument : userName")
        if passWord is None:
            return ("Missing arguement :passWord")
        if filePath is None:
            return ("Missing argument: filePath")
        if deLimiter is None:
            return ("Missing argument : deLimiter")
        var_command = "sh ver | i uptime"
        csv_content = []
        li = ["host name","IP Address","Uptime"]
        csv_content.append(li)
        try:
            fileObject=open(filePath,"r")
            text=fileObject.read()
            #print(text)
            if deLimiter == '\\n':
                return_list = text.splitlines()
            else:
                return_list = text.split(deLimiter)
            #print(return_list)
        except Exception as e:
            print('File Reading  exception: '+str(e),'ERROR')
            return {'Error while Reading a File ':str(e)}
        var_devices=return_list
        try:
            for var_foreach in str(var_devices).split(','):
                temp_output = var_foreach
                # previous_output = connectNetwork(r'cisco_ios',str(temp_output),22,str(userName),str(var_pass))
                network_connection = netmiko.ConnectHandler(r'cisco_ios',ip=str(temp_output),port=22,username=str(userName),password=str(passWord))
                execution_command = network_connection.send_command(str(var_command))
                if execution_command :
                    host_name = execution_command.split(" ")[0].strip()
                    #up_time = " ".join(x for x in previous_output.split(" ")[3:])
                    up_time = " ".join(x for x in execution_command.split(" ")[3:])
                    tmp_li = [host_name,var_foreach,up_time]
                    csv_content.append(tmp_li)
                    network_connection.disconnect()
                    continue
                else:
                    print('device not connected '+var_foreach,'IMP')
                    tmp_li = ["not connected",var_foreach,"not connected"]
                    csv_content.append(tmp_li)
                    continue
            with open('/tmp/network_files/net_info.csv','wb') as csv_file:
                cw = csv.writer(csv_file,quoting=csv.QUOTE_ALL)
            
            for line in csv_content:
                    cw.writerow(line)
            return {'Success':'Network UPtimes copied to a file '}
        except Exception as e :
            print("program terminated in connection and execution Commands")
            return {'Failure':'Network uptimes not copied '}

if __name__=="__main__":
    context={}
    bot_obj=CheckNetworkDeviceUpTime()
    
    context = {'userName':'','passWord':'','deLimiter':'','filePath':''}
    
    bot_obj.bot_init()
    output=bot_obj.execute(context)
    print(output)