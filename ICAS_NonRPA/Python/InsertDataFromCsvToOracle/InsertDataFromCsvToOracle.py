'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''

import cx_Oracle  
import csv
from abstract_bot import Bot

class InsertDataFromCsvToOracle(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext) :
        try: 
            
            csvPath = executeContext['csvPath']
            dbUsername = executeContext['dbUsername']
            dbPassword = executeContext['dbPassword']
            dbHost = executeContext['dbHost']
            tableName = executeContext['tableName']
                        
            if csvPath == '':
                return {'Exception' : 'missing argument csvPath'}  
            if dbUsername == '':
                return {'Exception' : 'missing argument dbUsername'}         
            if dbPassword == '':
                return {'Exception' : 'missing argument dbPassword'}
            if dbHost == '':
                return {'Exception' : 'missing argument dbHost'}
            if tableName == '':
                return {'Exception' : 'missing argument tableName'}  
           
            csvReader = csv.reader(open(csvPath,"r"))
            csvData=[]
            for line in csvReader:
                csvData.append(line)
            #print(csvData)
            colCount=0
            for element in csvData[0]:
                colCount+=1
            #print(colCount) 
            colValue=""
            for i in range(1,colCount+1):
                colValue+=":"+str(i)+","
                
            connString = '{0}/{1}@{2}'.format(dbUsername, dbPassword, dbHost)
            con = cx_Oracle.connect(connString)
            print("Successfully connected.")
            
            cur = con.cursor()  

            cur.executemany('INSERT INTO '+tableName+' VALUES('+colValue[:-1]+')',csvData[1:])
			#data to be entered excluding the headers from the csv file
            
			print("Data transferred succefully from CSV file to Oracle")
            
            con.commit()
            cur.close()
            con.close()
            return {'status' : 'success'}
        
        except cx_Oracle.DatabaseError as e: 
            return {'Exception' : str(e)}


if __name__ == '__main__':
    context = {}
    bot_obj = InsertDataFromCsvToOracle()

    context =  {
                'csvPath' : '',             #enter the path of csv file
                'dbUsername' : '',          #enter the db username
                'dbPassword' : '',          #enter the db password
                'dbHost' : '',              #enter the db host
                'tableName' : ''            #enter the table name in db where data needs to appended from csv file
                }
    '''
    #Sample input data
    context =  {
                'csvPath' : 'C:\\Users\\vikas.singh09\\Documents\\employee.csv',
                'dbUsername' : 'root',           
                'dbPassword' : 'secret',          
                'dbHost' : 'localhost',              
                'tableName' : 'employee'         
                }
    '''
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print('output : ',output)
