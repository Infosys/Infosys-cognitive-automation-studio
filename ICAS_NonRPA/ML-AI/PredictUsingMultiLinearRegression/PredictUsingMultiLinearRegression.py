'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn import datasets, linear_model
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score
from abstract_bot import Bot

class PredictUsingMultiLinearRegression(Bot):
    def bot_init(self):
        pass
    
    def execute(self, excecuteContext):
        try:
            trainData = excecuteContext['trainData']
            testData = excecuteContext['testData']
            outputFilePath = excecuteContext['outputFilePath']
            targetColumn = excecuteContext['targetColumn']

            if not trainData:
                return{'Missing Argument':'trainData'}
            if not testData:
                return{'Missing Argument':'testData'}
            if not outputFilePath:
                return{'Missing Argument':'outputFilePath'}
            if not targetColumn:
                return{'Missing Argument':'targetColumn'}

            le = LabelEncoder()
            oe= OneHotEncoder()
            train_data= pd.read_json(trainData)
            test_data= pd.read_json(testData)

            objList = train_data.select_dtypes(include = "object").columns
            
            #Label and One hot encoding categorical variables
            for col in objList:
                train_data[col] = le.fit_transform(train_data[col].astype(str))
                test_data[col] = le.fit_transform(test_data[col].astype(str))
                train_data[col] = le.fit_transform(train_data[col].astype(str))
                test_data[col] = le.fit_transform(test_data[col].astype(str))
    
            #Dropping categorical variables
            temp =pd.DataFrame(oe.fit_transform(train_data[objList]).toarray())
            train_data= train_data.drop(objList, axis=1)
            train_data= train_data.join(temp)

            #Dropping categorical variables
            temp =pd.DataFrame(oe.transform(test_data[objList]).toarray())
            test_data= test_data.drop(objList, axis=1).join(temp)

            train_X= train_data.drop(targetColumn, axis=1)
            train_y= train_data[targetColumn]
            test_X= test_data.drop(targetColumn, axis=1)
            test_y= test_data[targetColumn]

            #fitting regression model
            reg = LinearRegression().fit(train_X, train_y)
            test_y_pred= reg.predict(test_X)

            score= r2_score(test_y, test_y_pred)
            test_data= pd.read_json(testData)
            output_data= pd.concat([test_data, pd.DataFrame(test_y_pred, columns=['Prediction'])], axis= 1)
            # write predictions to a CSV file
            output_data.to_excel(outputFilePath, index=False)
#            joblib.dump(reg,executeContext['modelFileName'] + '.pkl')
           
            output= {'output':'Prediction File generated','r2_Score': score}
            return output
            
        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == '__main__':
    context = {}
    bot_obj = PredictUsingMultiLinearRegression()

    # --input parameters--
    context = {
            'trainData':'',
                'testData':'',
                'outputFilePath':"",
                'targetColumn': ""}

#            'trainData':r"D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\Maruthi AIML\Linearregression\train_regression.json",
#                'testData':r"D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\Maruthi AIML\Linearregression\test_regression.json",
#            'trainFilePath':r"D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\Maruthi AIML\Linearregression\ELMO_train.xlsx",
#                'testFilePath':r"D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\Maruthi AIML\Linearregression\ELMO_test.xlsx",
#                'outputFilePath':r"D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\Maruthi AIML\Linearregression\Output_elmo.xlsx",
#                'targetColumn': "Weight"}

    resp = bot_obj.execute(context)
    print('response : ',resp)












