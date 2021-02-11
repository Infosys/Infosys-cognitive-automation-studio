'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
import subprocess
from abstract_bot import Bot
class CheckPythonPkgVersion(Bot):
    
    def bot_init_(self):
        pass

    def execute(self,executionContext):
        try:    
            pythonPackageName = executionContext['pythonPackageName']
            if not pythonPackageName:
                return {'Warning':'Missing Argument pythonPackageName'}
            command = 'pip show ' + pythonPackageName
            process = subprocess.Popen(command.split(), stdout = subprocess.PIPE)
            stdout, stderr = process.communicate()
            stdout = ''.join(str(stdout)[1:])
            lines = stdout.split('\\r\\n')
            output = '' 
            for i in range (0, len(lines)):
                if 'Version' in lines[i]:
                    for j in lines[i].split()[1:2]:
                        output = j
            if output:
                output = 'Python Package : ' + pythonPackageName + ', Version : ' + output
                return {'Result': output}
            else:
                error ='Package(s) not found: '+pythonPackageName
                return {'Exception': error}
        except Exception as e:
            return {'Exception': str(e)} 
        
if __name__ == "__main__":
    context = {}
    bot_obj = CheckPythonPkgVersion()

    context = {'pythonPackageName':''}
    output = bot_obj.execute(context)
    print(output)     