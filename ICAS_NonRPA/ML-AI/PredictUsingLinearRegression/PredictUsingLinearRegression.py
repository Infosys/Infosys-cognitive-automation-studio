'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
import tensorflow as tf
import itertools
tf.compat.v1.disable_eager_execution()
from abstract_bot import Bot

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

class PredictUsingLinearRegression(Bot):
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
   
            train_data= pd.read_json(excecuteContext['trainData'])
            objList = train_data.select_dtypes(include = "object").columns

            test_data= pd.read_json(excecuteContext['testData'])
            objList_test = test_data.select_dtypes(include = "object").columns
           
            #Dropping categorical variables
            for col in objList:
                train_data[col] = le.fit_transform(train_data[col].astype(str))
                test_data[col] = le.fit_transform(test_data[col].astype(str))           
            temp =pd.DataFrame(oe.fit_transform(train_data[objList]).toarray())
            temp.columns =["dummy_"+str(x) for x in temp.columns]            
            train_data= train_data.drop(objList, axis=1)
            train_data= train_data.join(temp)
#            train_data= pd.concat([train_data]*30, ignore_index=True) 
            temp =pd.DataFrame(oe.fit_transform(test_data[objList_test]).toarray())
            temp.columns =["dummy_"+str(x) for x in temp.columns]
            test_data_bk= test_data
            test_data= test_data.drop(objList, axis=1)
            test_data= test_data.join(temp)
#            test_data= pd.concat([test_data]*30, ignore_index=True)
            COLUMNS = list(train_data.columns)  #['weight', 'lengtho', 'lengtht', 'lengthth', 'height', 'width']
            FEATURES = list(train_data.columns.drop(targetColumn))  #['lengtho', 'lengtht', 'lengthth', 'height', 'width']
            LABEL = targetColumn
            feature_cols = [tf.feature_column.numeric_column(k) for k in FEATURES]
            estimator = tf.estimator.LinearRegressor(feature_columns=feature_cols, model_dir="train_3")
            
            def get_input_fn(data_set, num_epochs=5000, n_batch = 128, shuffle=True):    
                     return tf.estimator.inputs.pandas_input_fn(       
                     x=pd.DataFrame({k: data_set[k].values for k in FEATURES}),  y = pd.Series(data_set[LABEL].values),       
                     batch_size=n_batch,  num_epochs=num_epochs, shuffle=shuffle)
            
            estimator.train(input_fn=get_input_fn(train_data, num_epochs=5000, n_batch = 128, shuffle=False), steps=None)
            ev = estimator.evaluate(input_fn=get_input_fn(train_data, num_epochs=5000, n_batch = 128, shuffle=False))
            
            loss_score = ev["loss"]
            #print("Loss: {0:f}".format(loss_score))
            
#            y = estimator.predict( input_fn=get_input_fn(train_data, num_epochs=5000, n_batch = 128,  shuffle=False))
#            
#            predictions = list(p["predictions"] for p in itertools.islice(y, 10))
#            print("Predictions: {}".format(str(predictions)))
            
            
            y = estimator.predict(input_fn=get_input_fn(test_data, num_epochs=5000, n_batch = 128,  shuffle=False))
#            predictions = list(p["predictions"] for p in itertools.islice(y, 10))
            y_pred= list(p["predictions"] for p in itertools.islice(y, test_data.shape[0]))
            y_pred= [x[0] for x in y_pred]
            y_test= test_data[targetColumn]
            
            Output_df= pd.concat([test_data_bk,pd.Series(y_pred,name='Predictions')], axis= 1)
            Output_df.to_excel(outputFilePath)
            output= {'output':'Prediction File generated','loss_score': int(loss_score)}
            return output
            
        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == '__main__':
    context = {}
    bot_obj = PredictUsingLinearRegression()

    context = {'trainData': '',
		       'testData': '',
#            		'trainData': '{\"Spec2\":{\"0\":\"Varisa\",\"1\":\"Varisa\",\"2\":\"Varisa\",\"3\":\"Varisa\",\"4\":\"Varisa\",\"5\":\"Varisa\",\"6\":\"Varisa\",\"7\":\"Varisa\",\"8\":\"Varisa\",\"9\":\"sepiosa\"},\"Species\":{\"0\":\"Bream\",\"1\":\"Bream\",\"2\":\"Bream\",\"3\":\"Bream\",\"4\":\"Bream\",\"5\":\"Bream\",\"6\":\"Bream\",\"7\":\"Bream\",\"8\":\"Bream\",\"9\":\"Bream\"},\"Weight\":{\"0\":242.0,\"1\":290.0,\"2\":340.0,\"3\":363.0,\"4\":430.0,\"5\":450.0,\"6\":500.0,\"7\":390.0,\"8\":450.0,\"9\":500.0},\"Length1\":{\"0\":23.2,\"1\":24.0,\"2\":23.9,\"3\":26.3,\"4\":26.5,\"5\":26.8,\"6\":26.8,\"7\":27.6,\"8\":27.6,\"9\":28.5},\"Length2\":{\"0\":25.4,\"1\":26.3,\"2\":26.5,\"3\":29.0,\"4\":29.0,\"5\":29.7,\"6\":29.7,\"7\":30.0,\"8\":30.0,\"9\":30.7},\"Length3\":{\"0\":30.0,\"1\":31.2,\"2\":31.1,\"3\":33.5,\"4\":34.0,\"5\":34.7,\"6\":34.5,\"7\":35.0,\"8\":35.1,\"9\":36.2},\"Height\":{\"0\":11.52,\"1\":12.48,\"2\":12.3778,\"3\":12.73,\"4\":12.444,\"5\":13.6024,\"6\":14.1795,\"7\":12.67,\"8\":14.0049,\"9\":14.2266},\"Width\":{\"0\":4.02,\"1\":4.3056,\"2\":4.6961,\"3\":4.4555,\"4\":5.134,\"5\":4.9274,\"6\":5.2785,\"7\":4.69,\"8\":4.8438,\"9\":4.9594}}',
#		          'testData': '{\"Spec2\":{\"0\":\"Varisa\",\"1\":\"Varisa\",\"2\":\"Varisa\",\"3\":\"Varisa\",\"4\":\"Varisa\",\"5\":\"Varisa\",\"6\":\"Varisa\",\"7\":\"Varisa\",\"8\":\"Varisa\",\"9\":\"sepiosa\"},\"Species\":{\"0\":\"Bream\",\"1\":\"Bream\",\"2\":\"Bream\",\"3\":\"Bream\",\"4\":\"Bream\",\"5\":\"Bream\",\"6\":\"Bream\",\"7\":\"Bream\",\"8\":\"Bream\",\"9\":\"Bream\"},\"Weight\":{\"0\":242.0,\"1\":290.0,\"2\":340.0,\"3\":363.0,\"4\":430.0,\"5\":450.0,\"6\":500.0,\"7\":390.0,\"8\":450.0,\"9\":500.0},\"Length1\":{\"0\":23.2,\"1\":24.0,\"2\":23.9,\"3\":26.3,\"4\":26.5,\"5\":26.8,\"6\":26.8,\"7\":27.6,\"8\":27.6,\"9\":28.5},\"Length2\":{\"0\":25.4,\"1\":26.3,\"2\":26.5,\"3\":29.0,\"4\":29.0,\"5\":29.7,\"6\":29.7,\"7\":30.0,\"8\":30.0,\"9\":30.7},\"Length3\":{\"0\":30.0,\"1\":31.2,\"2\":31.1,\"3\":33.5,\"4\":34.0,\"5\":34.7,\"6\":34.5,\"7\":35.0,\"8\":35.1,\"9\":36.2},\"Height\":{\"0\":11.52,\"1\":12.48,\"2\":12.3778,\"3\":12.73,\"4\":12.444,\"5\":13.6024,\"6\":14.1795,\"7\":12.67,\"8\":14.0049,\"9\":14.2266},\"Width\":{\"0\":4.02,\"1\":4.3056,\"2\":4.6961,\"3\":4.4555,\"4\":5.134,\"5\":4.9274,\"6\":5.2785,\"7\":4.69,\"8\":4.8438,\"9\":4.9594}}',

#	'trainData':'',#'{"spec":{"0":"sepiosa22","1":"Varisa","2":"Varisa","3":"Varisa","4":"Varisa","5":"Varisa","6":"Varisa","7":"Varisa","8":"Varisa","9":"sepiosa"},"species":{"0":"Bream","1":"Bream","2":"Bream","3":"Bream","4":"Bream","5":"Bream","6":"Bream","7":"Bream","8":"Bream","9":"Bream"},"weight":{"0":242.0,"1":290.0,"2":340.0,"3":363.0,"4":430.0,"5":450.0,"6":500.0,"7":390.0,"8":450.0,"9":500.0},"lengtho":{"0":24,"1":29.0,"2":33.9,"3":36.3,"4":42.5,"5":44.8,"6":49.8,"7":37.6,"8":45.6,"9":47.5},"lengtht":{"0":25.4,"1":26.3,"2":26.5,"3":29.0,"4":29.0,"5":29.7,"6":29.7,"7":30.0,"8":30.0,"9":30.7},"lengthth":{"0":30.0,"1":31.2,"2":31.1,"3":33.5,"4":34.0,"5":34.7,"6":34.5,"7":35.0,"8":35.1,"9":36.2},"height":{"0":11.52,"1":12.48,"2":12.3778,"3":12.73,"4":12.444,"5":13.6024,"6":14.1795,"7":12.67,"8":14.0049,"9":14.2266},"width":{"0":4.02,"1":4.3056,"2":4.6961,"3":4.4555,"4":5.134,"5":4.9274,"6":5.2785,"7":4.69,"8":4.8438,"9":4.9594}}',
#                'testData':'',#{"spec":{"0":"sepiosa22","1":"Varisa","2":"Varisa","3":"Varisa","4":"Varisa","5":"Varisa","6":"Varisa","7":"Varisa","8":"Varisa","9":"sepiosa"},"species":{"0":"Bream","1":"Bream","2":"Bream","3":"Bream","4":"Bream","5":"Bream","6":"Bream","7":"Bream","8":"Bream","9":"Bream"},"weight":{"0":242.0,"1":290.0,"2":340.0,"3":363.0,"4":430.0,"5":450.0,"6":500.0,"7":390.0,"8":450.0,"9":500.0},"lengtho":{"0":24,"1":29.0,"2":33.9,"3":36.3,"4":42.5,"5":44.8,"6":49.8,"7":37.6,"8":45.6,"9":47.5},"lengtht":{"0":25.4,"1":26.3,"2":26.5,"3":29.0,"4":29.0,"5":29.7,"6":29.7,"7":30.0,"8":30.0,"9":30.7},"lengthth":{"0":30.0,"1":31.2,"2":31.1,"3":33.5,"4":34.0,"5":34.7,"6":34.5,"7":35.0,"8":35.1,"9":36.2},"height":{"0":11.52,"1":12.48,"2":12.3778,"3":12.73,"4":12.444,"5":13.6024,"6":14.1795,"7":12.67,"8":14.0049,"9":14.2266},"width":{"0":4.02,"1":4.3056,"2":4.6961,"3":4.4555,"4":5.134,"5":4.9274,"6":5.2785,"7":4.69,"8":4.8438,"9":4.9594}}',
                'outputFilePath':"",
                'targetColumn': ""}

    resp = bot_obj.execute(context)
    print('response : ',resp)


