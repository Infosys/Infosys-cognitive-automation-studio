'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
##Convert CSV to JSON
#!/usr/bin/python
import csv , json
from files.abstract_bot import Bot

class CsvToJson(Bot):

    def bot_init(self):
        pass


    def execute(self, executeContext):
        try:
            csvFilePath = executeContext['csvFilePath']
            jsonFilePath = executeContext['jsonFilePath']
            arr = []

            #read the csv and add the arr to a arrayn
            with open (csvFilePath) as csvFile:
                csvReader = csv.DictReader(csvFile)
                for csvRow in csvReader:
                    arr.append(csvRow)

            # write the data to a json file
            with open(jsonFilePath, "w") as jsonFile:
                jsonFile.write(json.dumps(arr, indent = 4))

            return {'status':'success'}
        except Exception as e:
            return {'Exception':str(e)}

if __name__ == '__main__':
    context = {}
    output = {}
    obj_snow = CsvToJson()

    # file_json = open("D:\poc\SNOW_Bot\Ticket_details.json")
    context = {'csvFilePath' : "small.csv",'jsonFilePath' : "happy.json"}

    # print(dir(obj_snow))
    obj_snow.bot_init()
    output = obj_snow.execute(context)
    print(output)
    # write context to json