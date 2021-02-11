'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from __future__ import print_function
import psutil
from abstract_bot import Bot

class CheckPerformanceOfWindowsService(Bot):

    def bot_init(self):
        pass

    def execute(self, executeContext):
        service = None
        try:
            name = executeContext['name']
            service = psutil.win_service_get(name)
            service = service.as_dict()

            if service:
                print("Service found: ", service)
            else:
                print("Service not found")

            if service['status'] == 'running':
                print("Service is running")
            else:
                print("Service is not running")

            return service

        except Exception as e:
            return {'Exception': str(e)}

if __name__ == '__main__':
    context = {}
    bot_obj = CheckPerformanceOfWindowsService()

    context = {
        'name': ''

    }
    bot_obj.bot_init()
    output = bot_obj.execute(context)