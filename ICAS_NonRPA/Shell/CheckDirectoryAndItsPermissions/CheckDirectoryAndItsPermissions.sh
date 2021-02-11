:'
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'
#!/bin/bash

if [ $# -eq 0 ]; then
        echo "Error. Incorrect number of arguments passed to the script"
else
        while [ $# -gt 0 ];
        do
                case "$1" in
                        -sourceDirectory*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         sourceDirectory="${1#*=}"
                         ;;
                        -ProcessInstanceId*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         ProcessInstanceId="${1#*=}"
                         ;;
                        *)
                        echo "Error. Incorrect arguments passed to the script"
                        exit 1
                        ;;
                esac
                shift
        done
        if [[ -d "${sourceDirectory}" ]];then
                echo "sourceFile exists"
                if [[ -r ${sourceDirectory} ]];then
                        echo "successful"
                else
                        echo "failed"
                fi
                if [[ -w ${sourceDirectory} ]];then
                        echo "successful"
                else
                        echo "failed"
                fi
                if [[ -x ${sourceDirectory} ]];then
                        echo "successful"
                else
                        echo "failed"
                fi
        else
                echo "failed"
        fi
