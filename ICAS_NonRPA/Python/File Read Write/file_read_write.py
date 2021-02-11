'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# Auto generated - on: 20190401, by: vinay.reddy
# ------------------------------------------------------------------------------------------
# Variables and Libraries
import sys, re
previous_status = ""
previous_output = ""
sys.path.append(r"./Dependencies")
from Ops_Conn import *
# ------------------------------------------------------------------------------------------
# Arguments: ["string","file_path"]
# Test to read file using library
# ------------------------------------------------------------------------------------------
previous_status,arg_dict = readArguments('Script expects arguments')
if previous_status != 'OK':
	checkExit(1)
if "file_path" in arg_dict:
	file_path = arg_dict["file_path"]
else:
	printMsg('Missing argument: file_path','ERROR')
previous_status,previous_output = readFile(file_path)
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = printMsg(str(previous_output),r'IMP',r'NA')
if previous_status != 'OK':
	checkExit(1)
previous_status,previous_output = writeFile(str(previous_output),file_path)
if previous_status != 'OK':
	checkExit(1)
printMsg('Exiting.','INFO')
checkExit(0)
