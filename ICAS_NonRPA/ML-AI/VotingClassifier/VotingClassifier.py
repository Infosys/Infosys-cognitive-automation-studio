'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier
from sklearn.externals import joblib
from abstract_bot import Bot

class VotingClassifier(Bot):


    # def main(dataset,  target):
    def execute(self, executeContext):
        try:
            testSize = executeContext['testSize']
            randomState = executeContext['randomState']
            datasetFP = executeContext['datasetFP']
            targetFP = executeContext['targetFP']

            # --reading dataset from given file path--
            json_file = open(datasetFP, 'r')
            dataset = json_file.read()
            json_file = open(targetFP, 'r')
            target = json_file.read()

            X_train, X_test, y_train, y_test = train_test_split(dataset, target, test_size=testSize, random_state=randomState)
            xgb = xgb_model(X_train, y_train)
            rf =  rf_model(X_train,y_train)

            ensemble=VotingClassifier(estimators=[('XGBoost', xgb), ('Random Forest', rf)], 
            voting='soft', weights=[3,1]).fit(X_train,y_train)
            print('The accuracy for DecisionTree and Random Forest is:',ensemble.score(X_test,y_test))
            joblib.dump(ensemble, 'models/' + 'Voting_rf_xg_'+pred+'_' .pkl')
            return 'success'
        except Exception as e:
            return str(e)
        

    def xgb_model(self, tf_vec,y):
        xgb = XGBClassifier(n_estimators=int(100))
        return xgb.fit(tf_vec, y)
        
    def rf_model(self, tf_vec,y):
        rf = RandomForestClassifier(class_weight="balanced")
        return rf.fit(tf_vec,y)


# --for testing--
if __name__ == '__main__':
    context = {}
    bot_obj = VotingClassifier()

    # --input parameters--
    context = {'datasetFP':'', 'targetFP':'', 'testSize':0.15, 'randomState':42}

    bot_obj.bot_init()
    resp = bot_obj.execute(context)
    print('response : ',resp)

