'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
from abstract_bot import Bot  
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder  
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn import metrics 
     

class ValidateUsingKFold(Bot):

    def bot_init(self):
        pass

    def execute(self,executeContext):
        try:
            trainData = executeContext['trainData']
            testData = executeContext['testData']
            outputFilePath = executeContext['outputFilePath']
            targetColumn = executeContext['targetColumn']
            classifier = executeContext['classifier']

            le = LabelEncoder()
            oe= OneHotEncoder()
            train_data= pd.read_csv(trainData)
            test_data= pd.read_csv(testData)

            objList = train_data.select_dtypes(include = "object").columns

            for col in objList:
                train_data[col] = le.fit_transform(train_data[col].astype(str))
                test_data[col] = le.fit_transform(test_data[col].astype(str))

            temp =pd.DataFrame(oe.fit_transform(train_data[objList]).toarray())
            train_data= train_data.drop(objList, axis=1)
            train_data= train_data.join(temp)

            temp =pd.DataFrame(oe.transform(test_data[objList]).toarray())
            test_data= test_data.drop(objList, axis=1).join(temp)

            train_X= train_data.drop(targetColumn, axis=1)
            train_y= train_data[targetColumn]
            test_X= test_data.drop(targetColumn, axis=1)
            test_y= test_data[targetColumn]   

            sc = StandardScaler()
            train_X = sc.fit_transform(train_X)
            test_X = sc.transform(test_X)

            if classifier == 'LogisticRegression':
                classifier = LogisticRegression(random_state = 0)
                classifier.fit(train_X, train_y)

            if classifier == 'DecisionTreeClassifier':
                classifier = DecisionTreeClassifier(random_state = 0)
                classifier.fit(train_X, train_y)    
            
            if classifier == 'RandomForestClassifier':
                classifier = RandomForestClassifier(n_estimators=100,criterion='entropy',random_state = 0)
                classifier.fit(train_X, train_y)

            if classifier == 'XGBClassifier':
                classifier = XGBClassifier()
                classifier.fit(train_X, train_y)      


            y_pred = classifier.predict(test_X)
            from sklearn.model_selection import cross_val_score
            accuracies = cross_val_score(estimator = classifier, X = train_X, y = train_y, cv = 10)

            output_data= pd.concat([test_data, pd.DataFrame(y_pred, columns=['Prediction'])], axis= 1)
            output_data.to_excel(outputFilePath, index=False)

            return {'output':'Predicted values generated',
                    'Accuracy_mean' : accuracies.mean() ,
                    'Accuracy_std' : accuracies.std(),
            }


        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == "__main__":
    context = {
                #'trainData':'C:/Users/sidhartha.samal/Desktop/Wine1.csv',
                #'testData':'C:/Users/sidhartha.samal/Desktop/Wine2.csv',
                #'outputFilePath':"C:/Users/sidhartha.samal/Desktop/Wine_prediction.xlsx",
                #'targetColumn': "Customer_Segment",
                #'classifier' : 'XGBClassifier'
				
				'trainData':'',
                'testData':'',
                'outputFilePath':'',
                'targetColumn': '',
                'classifier' : ''
    }
    bot_obj = ValidateUsingKFold()
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
