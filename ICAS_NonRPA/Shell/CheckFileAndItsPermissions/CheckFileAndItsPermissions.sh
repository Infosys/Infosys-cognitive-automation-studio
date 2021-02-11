:'
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'
#!/bin/bash
if [ $# -lt 1 ]; then
        echo "Error. Incorrect number of arguments passed to the script"
        exit 1
else
        while [ $# -gt 0 ];
        do
                case "$1" in
                        -sourceFile*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         sourceFile="${1#*=}"
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
        if [[ -e "${sourceFile}" ]];then
                echo "sourceFile exists"
                if [[ -r ${sourceFile} ]];then
                        echo "successful"
                else
                        echo "failed"
                fi
                if [[ -w ${sourceFile} ]];then
                        echo "successful"
                else
                        echo "failed"
                fi
                if [[ -x ${sourceFile} ]];then
                        echo "successful"
                else
                        echo "failed"
                fi
        else
                echo "failed"
        fi
