:'
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'
#!/bin/sh
filePath=$1
if [ $# -lt 1 ]
then
        echo "Error: Incorrect number of arguments passed to the script"
        exit 1
else
        while [ $# -gt 0 ];
                do
                case "$1" in
                        -filePath*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         filePath="${1#*=}"
                         ;;
                        -ProcessInstanceId*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         ProcessInstanceId="${1#*=}"
                         ;;
                esac
                shift
        done
                if [ -z "${filePath}" ]
        then
                echo "Error: File path is empty"
                exit 1
                else
                if [ -f "${filePath}" ]; then
                                        if [ ! -r "${filePath}" ]; then
                        echo "Error: Cannot read file '${filePath}'"
                                                exit 1
                                        fi
                                        if [ "$(file $filePath)" != "$filePath: ASCII text" ]; then
                        echo "Error: Not an ASCII text file"
                                                exit 1
                                        fi
                                        echo "Contents of file '${filePath}' are: "
                                        echo $(cat $filePath)
                                        if [ $? == 0 ]
                                        then
                                                echo "Status: Success"
                                                exit 0
                                        fi
                                else
                                        echo "Error: No such file"
                                        exit 1
                                fi
        fi
fi
