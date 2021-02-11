'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# Auto generated - on: 20190723, by: akhil.krishna
# ------------------------------------------------------------------------------------------
# Variables and Libraries
import sys, re, os
# from Ops_Conn import *
from abstract_bot import Bot
# ------------------------------------------------------------------------------------------
# Arguments: ["string","file_path"]
# deletes a file
# ------------------------------------------------------------------------------------------
class DeleteFile(Bot):


  def bot_init(self):
    pass


  def execute(self, executeContext):
    # self.previous_status,self.arg_dict = readArguments('Script expects arguments')
    # if responseprevious_status != 'OK':
      # checkExit(1)
    if "file_path" in executeContext:
      file_path = executeContext["file_path"]
    else:
      return {'Missing argument': 'file_path'}
    try:
      os.remove(file_path)

      return {'status' : 'success'}
    except Exception as e:
      return {'Exception' : str(e)}

    

if __name__ == '__main__':
    context = {}
    output = {}
    obj_snow = DeleteFile()

    context = {'file_path':'D:\\Dummy\\delete\\new.txt'}

    # print(dir(obj_snow))
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
    # write context to json

