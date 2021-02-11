'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# Auto generated - on: 20180417, by: vinay.reddy
# ------------------------------------------------------------------------------------------
# Variables and Libraries
import sys, re
previous_status = ""
previous_output = ""
sys.path.append(r"./Dependencies")
from Ops_Conn import *
# ------------------------------------------------------------------------------------------
# Arguments: 
# Network DHCP Configuration
# ------------------------------------------------------------------------------------------
previous_status,previous_output = connectNetwork(r'cisco_ios',r'device01',22,r'NO',r'user_name',r'NA')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'ip dhcp excluded-address 192.168.101.254',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'ip dhcp ping packets 3',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'ip dhcp ping timeout 1000',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'ip dhcp pool VOICE-LAN-Pool',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'ip dhcp pool VOICE-LAN-Pool',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'import all',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'network 192.168.101.0 255.255.255.0',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'default-router 192.168.101.254',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'dns-server 8.8.8.8 4.4.4.4',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'option 42 ip 192.168.101.254',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'option 150 ip 10.10.10.10 10.10.11.10',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'option 66 ascii dms.xyzbusiness.abc.com',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'option 160 ascii http://poldms.xyzbusiness.abc.com/dms/bootstrap',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'lease 7',r'YES')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = executeNetwork(r'show run | include dhcp',r'NO')
if previous_status != 'OK':
	checkExit(1)
printMsg('Return value: '+str(previous_output))
if previous_output and re.search('dhcp',str(previous_output),re.IGNORECASE):
	printMsg('IF condition matches','INFO')
	previous_status,previous_output = printMsg(str(previous_output),r'IMP',r'DHCP pool config done:')
	if previous_status != 'OK':
		checkExit(1)
	printMsg('Exiting.','INFO')
	checkExit(0)
else:
	printMsg('ELSE condition','INFO')
	previous_status,previous_output = printMsg(str(previous_output),r'ERROR',r'DHCP pool config error:')
	if previous_status != 'OK':
		checkExit(1)
	printMsg('Aborting!','ERROR')
	checkExit(1)
