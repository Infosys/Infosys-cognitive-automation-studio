'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import traceback
import sys
import pickle
from abstract_bot import Bot

# -- bot for Exporting file names from given directory --
class ExportingPickle(Bot):


    def bot_init(self):
        pass

    def execute(self, executionContext):
        try:
            file_path = executionContext['pickle_file_path']
            file_name = executionContext['pickle_name']

            example_dict = {1:"6",2:"2",3:"f"}

            pickle_out = open(file_path +'/'+ file_name,"wb")
            pickle.dump(example_dict, pickle_out)
            pickle_out.close()
            return {'output':'Pickle file Exported successfully'}
        except:
          exc_type, exc_value, exc_traceback = sys.exc_info()
          formatted_lines = traceback.format_exc().splitlines()
          return {'Error' : formatted_lines[-1]} 

if __name__ == "__main__":
    context = {}
    bot_obj = ExportingPickle()

    #context = {'pickle_file_path':'D:\\Bot_Factory\\microbots\\GenericBots\\ExportingPickle','pickle_name':'sample.pkl'}
    context = {'pickle_file_path':'','pickle_name':''}

    bot_obj.bot_init()
    output = bot_obj.execute(context)
    #print(output)