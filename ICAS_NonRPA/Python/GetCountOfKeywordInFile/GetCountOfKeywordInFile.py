'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import re
from abstract_bot import Bot

# Bot to count a given keyword in an input file
# Input Parameters : input file path, keyword to be searched
# returns the count of the keyword in the file


class GetCountOfKeywordInFile(Bot):

    def bot_init(self):
        pass

    # execute method with main functionality
    def execute(self, executeContext):
        try:

            if 'inputFilePath' in executeContext and 'keywordPattern' in executeContext:
                inputFilePath = executeContext['inputFilePath']
                keywordPattern = executeContext['keywordPattern']
                with open(inputFilePath, "r") as inputFile:
                    inputContent = inputFile.read()
                    keywordCount = len(re.findall(r'\b'+keywordPattern+r'\b', inputContent))

                    # return count and success status if keyword was found in input file

                    if keywordCount > 0:
                        print("keyword '{}' was found {} times in the input file".format(keywordPattern, keywordCount))
                        return {'status': 'success'}
                    else:
                        return {'Exception': 'no match found'}
                inputFile.close()

            # throw exception if input parameters are not passed
            else:
                return {'Exception': 'missing argument'}

        except Exception as e:
            return {'Exception': str(e)}


if __name__ == "__main__":
    #context = {"inputFilePath":"C:\\Users\\aishwarya_padhi\\Desktop\\samplePythonBot\\count_keyword_input.txt","keywordPattern":"sea"}
    context = {"inputFilePath": "", "keywordPattern": ""}
    output = {}
    obj1 = GetCountOfKeywordInFile()
    obj1.bot_init()
    output = obj1.execute(context)
    print(output)




