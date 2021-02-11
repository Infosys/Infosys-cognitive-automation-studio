import os
import shutil
import traceback
import sys
from abstract_bot import Bot
import json


class RemoveHeaderFromCsv(Bot):

    def bot_init(self):
        pass

    def execute(self, executionContext):
        try:
            executionContext = json.dumps(executionContext)
            executionContext = json.loads(executionContext)
            inputFile = executionContext['inputFile']
            output_file_path = os.path.dirname(inputFile)
            outputFile = '{0}\{1}'.format(output_file_path, "outputFile.csv")
            shutil.copy(inputFile, outputFile)

            with open(outputFile) as f:
                first = f.read(1)
                if not first:
                    return {'Failure': 'file is empty'}
                else:
                    with open(outputFile, 'r+') as fd:
                        pos = fd.tell()
                        fd.readline()
                        rest = fd.read()
                        fd.seek(pos)
                        fd.truncate()
                        fd.write(rest)
                    return {'outputFile': outputFile}
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_lines = traceback.format_exc().splitlines()
            return {'Failure': formatted_lines[-1]}


if __name__ == "__main__":
    context = {}
    bot_obj = RemoveHeaderFromCsv()

    context = {'inputFile': r''}
    bot_obj.bot_init()
    output = bot_obj.execute(context)
    print(output)
