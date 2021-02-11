:'
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'
#!/bin/sh

if [ $# -lt 3 ]
then
        echo "Error. Incorrect number of arguments passed to the script"
        exit
else
        while [ $# -gt 0 ];
        do
                case "$1" in
                        -logfilePath*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         logfilePath="${1#*=}"
                         ;;
                        -logfileName*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         logfileName="${1#*=}"
                         ;;
                        -logMsg*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         logMsg="${1#*=}"
                         ;;
                        -ProcessInstanceId*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         ProcessInstanceId="${1#*=}"
                         ;;
                        *)
                        echo "Error. Incorrect arguments passed to the script"
                        exit
                        ;;
                esac
                shift
        done

#check if input parameters are passed correctly
if [[ -z "${logfilePath}"  ||  -z "${logfileName}"  || -z "${logMsg}" ]]
then
        echo "Error. Input parameters invalid."
        exit
else
        touch "${logfilePath}/${logfileName}"
        echo ${logMsg} >> "${logfilePath}/${logfileName}"
        echo $?
        if [ $? -eq 0 ]
        then
                echo "message logged successfully."
        fi
fi
fi