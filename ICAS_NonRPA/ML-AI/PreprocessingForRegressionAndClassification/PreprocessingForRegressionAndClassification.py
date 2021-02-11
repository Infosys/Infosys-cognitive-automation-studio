'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
import numpy as np
from abstract_bot import Bot
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.base import TransformerMixin
import json

class PreprocessingForRegressionAndClassification(Bot,TransformerMixin):

    def bot_init(self):
        pass      

    def fit(self, X, y=None):

        self.fill = pd.Series([X[c].value_counts().index[0]
        if X[c].dtype == np.dtype('O') else X[c].mean() for c in X],index=X.columns)
        return self

    def transform(self, X, y=None):
        return X.fillna(self.fill)    
    
    def execute(self,executeContext):
        try:
            inputData = executeContext['inputData']
            targetColumn = executeContext['targetColumn']
            scalingNeeded = executeContext['scalingNeeded']

            if not inputData:
                return {'Missing argument': 'inputData'}
            if not targetColumn:
                return {'Missing argument' :'targetColumn'}
            if not scalingNeeded:
                return {'Missing argument' :'scalingNeeded'}

            inputData= pd.read_csv(inputData)
            X = inputData.drop(targetColumn, axis=1)
            y = inputData[targetColumn]             

            if (X.isnull().any().sum() > 0):
                X = Preprocessing().fit_transform(X)

            X_numeric = X._get_numeric_data()

            le = LabelEncoder()
            oe= OneHotEncoder()

            X=pd.DataFrame(X)
            y=pd.DataFrame(y)

            objList_X = X.select_dtypes(include = "object").columns

            for col in objList_X:
                X[col] = le.fit_transform(X[col].astype(str))
            if len(objList_X)>0:
                temp =pd.DataFrame(oe.fit_transform(X[objList_X]).toarray())
                X= X.drop(objList_X, axis=1)
                X= X.join(temp)
                
            X_train, X_test, y_train, y_test =  train_test_split(X,y,test_size = 0.2, random_state= 0)

            if (scalingNeeded == 'yes'):
                X_train = X_train.copy()
                X_test = X_test.copy()
                from sklearn.preprocessing import StandardScaler
                for i in X_numeric:
                    scale = StandardScaler().fit(X_train[[i]])
                    X_train[i] = scale.transform(X_train[[i]])
                    X_test[i] = scale.transform(X_test[[i]])

            X_train = X_train.to_json()
            X_test = X_test.to_json()
            y_train = y_train.to_json()
            y_test = y_test.to_json()        
            

            return {'Success':'Preprocessed files generated successfully',
                    'trainX':X_train,
                    'trainY':y_train,
                    'testX':X_test,
                    'testY':y_test}    
            
        except Exception as e:
            return {'Exception': str(e)}

if __name__ == '__main__':
    context = {}
    bot_obj = PreprocessingForRegressionAndClassification()

    context = {
                'inputData':'',
                'targetColumn': '',
                'scalingNeeded': ''    }
        
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
