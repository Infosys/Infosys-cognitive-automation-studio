'''
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'''
from win32com.client import Dispatch
from files.abstract_bot import Bot

class CountOfUnReceivedReplyEmails(Bot):
    def bot_init_(self):
        pass

    def execute(self, executionContext):
        try:
            outlook = Dispatch("Outlook.Application").GetNamespace("MAPI")
            sent = outlook.GetDefaultFolder(5)
            smessages = sent.Items
            inbox = outlook.GetDefaultFolder(6)
            rmessages = inbox.Items
            unReceivedReply = []
            for rm in rmessages:
                if rm.Subject[0:3] == "Re:" or rm.Subject[0:3] == "RE:":
                    for sm in smessages:
                        if sm.Subject != rm.Subject[4:] or rm.Subject != sm.Subject:
                            if sm.Subject not in unReceivedReply:
                                unReceivedReply.append(sm.Subject)
            outputStatus = 'Total number of sent emails user not received a reply for are ' + str(len(unReceivedReply))
            return {'Status': outputStatus}
        except Exception as e:
            return {'Exception': str(e)}


if __name__ == "__main__":
    context = {}
    bot_obj = CountOfUnReceivedReplyEmails()

    output = bot_obj.execute(context)
    print(output)
