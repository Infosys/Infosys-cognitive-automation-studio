'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# -*- coding: utf-8 -*-
'''
---------------------------------------------------------------------------------
This bot search for a keyword in  a given log file.
---------------------------------------------------------------------------------
Author  : rahul.singh78@infosys.com
---------------------------------------------------------------------------------
Date    : 14-Mar-2020
---
'''

import sys
import traceback
import re
import os


from abstract_bot import Bot
class SearchLogFile(Bot):
    def bot_init(self):
        pass

    def execute(self, executionContext):

        try:
            inputFile = executionContext["inputFile"]
            keyword = executionContext["keyword"]
            output_file_path = os.path.dirname(inputFile)
            outputFile = '{0}\{1}'.format(output_file_path, "outputFile.txt")
            text = open(inputFile, 'r')
            sentences = re.split(r'[\n]+', text.read())
            res = [i for i in sentences if re.search(r'%s' % keyword.lower(), i.lower())]
            final = open(outputFile, 'w+')
            final.write("\n".join(res))
            return {'OutputFile': outputFile}

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Failure': formatted_lines[-1]}


if __name__ == "__main__":
    context = {}
    bot_obj = SearchLogFile()

    context = {'inputFile': r'',
               'keyword': r''
               }

    # Passing input parameters in the context below.
    bot_obj.bot_init()
    result = bot_obj.execute(context)
    print(result)
