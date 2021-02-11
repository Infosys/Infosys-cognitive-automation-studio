:'
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'
#!/bin/sh
var=$1
if [ $# -lt 1 ]
then
        echo "Error: Incorrect number of arguments passed to the script"
        exit 1
else
        while [ $# -gt 0 ];
                do
                case "$1" in
                        -var**)
                         if [[ "$1" != *=* ]]; then shift; fi
                         var="${1#*=}"
                         ;;
                        -ProcessInstanceId*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         ProcessInstanceId="${1#*=}"
                         ;;
                esac
                shift
        done
        if ! [[ "$var" =~ ^[0-9]+$ ]]; then
                echo "failed"
        else
                echo "successful"
        fi
fi
