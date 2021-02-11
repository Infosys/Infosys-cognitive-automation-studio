'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
# Importing the libraries
import pandas as pd
from abstract_bot import Bot
from apyori import apriori

class PredictUsingApriori(Bot):
    def bot_init(self):
        pass
    
    def execute(self, excecuteContext):
        try:
            inputFileName = excecuteContext["inputFileName"]
            minSupport = excecuteContext['minSupport']
            minConfidence = excecuteContext["minConfidence"]
            minLift = excecuteContext["minLift"]
            destFile = excecuteContext["destFile"]

            # Data Preprocessing
            inputFileName = pd.read_csv(inputFileName,header=None)
            df = pd.DataFrame(inputFileName)                 
            rows=len(df.axes[0])
            cols=len(df.axes[1])

            transactions = []
            for i in range(0, rows):
                transactions.append([str(inputFileName.values[i,j]) for j in range(0, cols)])

            # Training Apriori on the inputFileName
            rules = apriori(transactions, min_support = float(minSupport), min_confidence = float(minConfidence), min_lift = int(minLift), min_length = 2)

            # Visualising the results
            results = list(rules)

            # Displaying the results non sorted
            def inspect(results):
                lhs = [tuple(result[2][0][0])[0] for result in results]
                rhs = [tuple(result[2][0][1])[0] for result in results]
                supports = [result[1] for result in results]
                confidences = [result[2][0][2] for result in results]
                lifts = [result[2][0][3] for result in results]
                return list(zip(lhs,rhs,supports,confidences,lifts))
            resultsinDataFrame = pd.DataFrame(inspect(results),columns = ['Left Hand side','Right Hand side','Support','Confidence','Lift'])
            resultsinDataFrame.to_excel(destFile, index=False)

            
            inspect = inspect(results)
            return {'Success' : 'Results validated'}

        except Exception as e:
            return {'Exception' : str(e)}

if __name__ == '__main__':
    context = {}
    bot_obj = PredictUsingApriori()

    context = {'inputFileName': "",
               'minSupport' : '',
               'minConfidence' : '',
               'minLift' : '',
               'destFile' : '', 
                    }
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)


