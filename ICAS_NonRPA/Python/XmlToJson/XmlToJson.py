'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import os
import sys
import traceback
import json

from abstract_bot import Bot
import xmltodict


class XmlToJson(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):

        if "xmlFile" in executeContext:
            xml_file = executeContext["xmlFile"]
            output_file_path = os.path.dirname(xml_file)
            jsonFile = '{0}\{1}'.format(output_file_path, "jsonFile.json")
        else:
            return {'Missing argument': 'inputFile'}

        try:
            # Read the xml file
            with open(xml_file) as xml_file:
                data_dict = xmltodict.parse(xml_file.read())
                xml_file.close()
                json_data = json.dumps(data_dict)

                with open(jsonFile, "w") as json_file:
                    json_file.write(json_data)
                    json_file.close()

            return {'jsonFile': jsonFile}
        except Exception as e:
            return {'Exception': str(e)}


if __name__ == "__main__":
    context = {}
    output = {}
    bot_obj = XmlToJson()

    # context = {'xmlFile': r'D:\Bot Mela\BOTCodeAccelerate\XmlToJson\input.xml'}
    context = {'xmlFile': r''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
