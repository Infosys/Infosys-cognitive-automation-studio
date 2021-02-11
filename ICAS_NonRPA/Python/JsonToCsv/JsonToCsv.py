'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
##Convert CSV to JSON
#!/usr/bin/python

import csv, json
import pandas as pd
from abstract_bot import Bot

class JsonToCsv(Bot):

	def bot_init(self):
		pass


	def execute(self, executeContext):
		try:
			csvFilePath = executeContext['csvFilePath']
			jsonFilePath = executeContext['jsonFilePath']


			df = pd.read_json(jsonFilePath, encoding="utf8")
			df.to_csv (csvFilePath, index = None)
			#inputFile = open(jsonFilePath) #open json file
			#outputFile = open(csvFilePath, 'w',newline='') #load csv file
			#data = json.load(inputFile) #load json content
			#inputFile.close() #close the input file
			#output = csv.writer(outputFile) #create a csv.write
			#output.writerow(data[0].keys())  # header row
			#for row in data:
			#	print(row)
			#	output.writerow(row.values()) #values row
			return {'status' : 'success'}
		except Exception as e:
			return {'Exception' : str(e)}

if __name__ == '__main__':
	context = {}
	output = {}
	obj_snow = JsonToCsv()

	context = {'csvFilePath' : "",'jsonFilePath' : ""}

	# print(dir(obj_snow))
	obj_snow.bot_init()
	output = obj_snow.execute(context)
	print(output)
	# write context to json