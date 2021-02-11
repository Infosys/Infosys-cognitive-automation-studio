'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import pandas as pd
from abstract_bot import Bot   
from sklearn.preprocessing import StandardScaler
import json 
from sklearn.decomposition import PCA

class ReduceDimensionsUsingPCA(Bot):

    def bot_init(self):
        pass

    def execute(self,executeContext):
        try:
            inputData = executeContext['inputData']
            targetColumn = executeContext['targetColumn']

            input_data= pd.read_csv(inputData)
            X = input_data.drop(targetColumn, axis=1)
            y = input_data[targetColumn]

            # Feature Scaling
            sc = StandardScaler()
            X = sc.fit_transform(X)
        
            pca = PCA(n_components = 2)
            X = pca.fit_transform(X)
            explained_variance = pca.explained_variance_ratio_            
            explained_variance = explained_variance.tolist()
            json_str = json.dumps(explained_variance)
            return {'First & second highest variance': json_str}

        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == "__main__":
    context = {
                'inputData':'',
                'targetColumn': ""
    }
    bot_obj = ReduceDimensionsUsingPCA()
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
