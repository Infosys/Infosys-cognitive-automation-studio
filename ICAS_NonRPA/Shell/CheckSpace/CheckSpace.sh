:'
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'
#!/bin/sh
directory="$1"
requiredSpace="$2"

if [ $# -lt "2" ]
then
        echo "Error. Incorrect number of arguments passed to the script"
        exit 1
else
        while [ $# -gt 0 ];
        do
                case "$1" in
                        -directory*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         directory="${1#*=}"
                         ;;
                        -requiredSpace*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         requiredSpace="${1#*=}"
                         ;;
                        -ProcessInstanceId*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         ProcessInstanceId="${1#*=}"
                         ;;
                esac
                shift
        done
fi


if [ -z ${directory} ]
then
        echo "Path is empty"
elif [ ! -d ${directory} ]
then
        echo "Invalid directory"
elif [ -z ${requiredSpace} ]
then
        echo "Please give the required space in Kb"
elif [ ${requiredSpace} -le 0 ]
then
        echo "Space required ${requiredSpace}Kb should be numeric"
else
        available_space=$(df -k ${directory} | tail -1 | awk '{print $4}')
        if [ ${available_space} -le ${requiredSpace} ]; then
                echo "Not enough disk space."
        else [ ${available_space} -gt ${requiredSpace} ];
                 echo "The available disk space is ${available_space} Kb."
        fi
                        if [ $? != 0 ]
                                then
                                        echo "Error. Command execution failed."
                                else
                                        echo "Command executed successfully."
                        fi
        fi
