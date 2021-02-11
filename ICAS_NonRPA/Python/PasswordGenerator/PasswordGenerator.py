'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os  # Library1 for our usage
import traceback  # Library2 for our usage
import sys  # Library3 for our usage
import random  # Library4 for our usage
import json  # Library5 for our usage
from abstract_bot import Bot

# -- Bot for Strong Password Generation --

class PasswordGenerator(Bot):

    def bot_init(self):
        pass

    def execute(self, context):
        try:

            digits = "0123456789"
            Mixed = "ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyz@#!$0123456789"
            Upr_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            Lwr_case = "abcdefghijklmnopqrstuvwxyz"
            Spcl_char = "@#!$"
            length = context["passwordLength"]
            length_in = int(length.strip() or 0)

            if length_in >= 8 and length_in <= 12:
                p = "".join(random.sample(Upr_case, 1)) + "".join(random.sample(digits, 1)) + "".join(
                    random.sample(Lwr_case, 1)) + "".join(random.sample(Spcl_char, 1)) + "".join(
                    random.sample(Mixed, length_in - 4))
                output_value = json.dumps(p)
                return {'password': output_value}

            else:
                return {'result': "Minimum and maximum allowed password length is 8 and 12 respectively"}

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Error': formatted_lines[-1]}


if __name__ == "__main__":
    context = {}

    bot_obj = PasswordGenerator()  # Instantiating the class object

    # Passing input parameters in the context below.

    context = {"passwordLength": ''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)

    # print the returning output from after execution
    print(output)
