'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import numpy as np
#from sklearn.linear_model import LinearRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn import datasets, linear_model
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import f1_score
from abstract_bot import Bot

class PredictUsingNaiveBayesAlgorithm(Bot):
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
            #since this is classification
            objList = train_data.select_dtypes(include = "object").columns.drop(targetColumn)
            
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
            reg = MultinomialNB().fit(train_X, train_y)
            test_y_pred= reg.predict(test_X)

            score= f1_score(test_y, test_y_pred,average='micro')
            test_data= pd.read_json(testData)
            output_data= pd.concat([test_data, pd.DataFrame(test_y_pred, columns=['Prediction'])], axis= 1)
            # write predictions to a CSV file
            output_data.to_excel(outputFilePath, index=False)
#            joblib.dump(reg,executeContext['modelFileName'] + '.pkl')           
            output= {'output':'Prediction File generated','F1_Score': score}
            return output
            
        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == '__main__':
    context = {}
    bot_obj = PredictUsingNaiveBayesAlgorithm()

    # --input parameters--
    context = {'trainData':'',
               'testData':'',
               'outputFilePath':"",
               'targetColumn': ""}

#            'trainData':'{"Spec2":{"0":"sepiosa22","1":"Varisa","2":"Varisa","3":"Varisa","4":"Varisa","5":"Varisa","6":"Varisa","7":"Varisa","8":"Varisa","9":"sepiosa"},"Species":{"0":"Bream","1":"Bream","2":"Bream","3":"Bream","4":"Bream","5":"Bream","6":"Bream","7":"Bream","8":"Bream","9":"Bream"},"Weight":{"0":242.0,"1":290.0,"2":340.0,"3":363.0,"4":430.0,"5":450.0,"6":500.0,"7":390.0,"8":450.0,"9":500.0},"Length1":{"0":23.2,"1":24.0,"2":23.9,"3":26.3,"4":26.5,"5":26.8,"6":26.8,"7":27.6,"8":27.6,"9":28.5},"Length2":{"0":25.4,"1":26.3,"2":26.5,"3":29.0,"4":29.0,"5":29.7,"6":29.7,"7":30.0,"8":30.0,"9":30.7},"Length3":{"0":30.0,"1":31.2,"2":31.1,"3":33.5,"4":34.0,"5":34.7,"6":34.5,"7":35.0,"8":35.1,"9":36.2},"Height":{"0":11.52,"1":12.48,"2":12.3778,"3":12.73,"4":12.444,"5":13.6024,"6":14.1795,"7":12.67,"8":14.0049,"9":14.2266},"Width":{"0":4.02,"1":4.3056,"2":4.6961,"3":4.4555,"4":5.134,"5":4.9274,"6":5.2785,"7":4.69,"8":4.8438,"9":4.9594}}',
#                'testData':'{"Spec2":{"0":"Varisa","1":"Varisa","2":"sepiosa22","3":"Varisa","4":"Varisa","5":"Varisa","6":"Varisa","7":"Varisa","8":"Varisa","9":"sepiosa"},"Species":{"0":"Bream","1":"Bream","2":"Bream","3":"Bream","4":"Bream","5":"Bream","6":"Bream","7":"Bream","8":"Bream","9":"Bream"},"Weight":{"0":242.0,"1":290.0,"2":340.0,"3":363.0,"4":430.0,"5":450.0,"6":500.0,"7":390.0,"8":450.0,"9":500.0},"Length1":{"0":23.2,"1":24.0,"2":23.9,"3":26.3,"4":26.5,"5":26.8,"6":26.8,"7":27.6,"8":27.6,"9":28.5},"Length2":{"0":25.4,"1":26.3,"2":26.5,"3":29.0,"4":29.0,"5":29.7,"6":29.7,"7":30.0,"8":30.0,"9":30.7},"Length3":{"0":30.0,"1":31.2,"2":31.1,"3":33.5,"4":34.0,"5":34.7,"6":34.5,"7":35.0,"8":35.1,"9":36.2},"Height":{"0":11.52,"1":12.48,"2":12.3778,"3":12.73,"4":12.444,"5":13.6024,"6":14.1795,"7":12.67,"8":14.0049,"9":14.2266},"Width":{"0":4.02,"1":4.3056,"2":4.6961,"3":4.4555,"4":5.134,"5":4.9274,"6":5.2785,"7":4.69,"8":4.8438,"9":4.9594}}',
#                'outputFilePath':r"D:\OneDrive - Infosys Limited\botfactory\Ajay Testing Bots\Maruthi AIML\Linearregression\Output_regression1.xlsx",
#                'outputFilePath':r"D:\Output_regression1.xlsx",
#                'targetColumn': "Spec2"}
    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)