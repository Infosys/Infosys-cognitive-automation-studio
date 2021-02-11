:'
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'
#!/bin/sh

if [ $# -lt "1" ]
then
        echo "Error. Incorrect number of arguments passed to the script"
        exit 1
else
        while [ $# -gt 0 ];
        do
                case "$1" in
                        -vString*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         vString="${1#*=}"
                         ;;
                        -ProcessInstanceId*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         ProcessInstanceId="${1#*=}"
                         ;;
                esac
                shift
        done
fi

if [ -z "${vString}" ] ; then
String_Length=0
        echo "Please enter the String"
else

  String_Length=`echo "${vString}" | awk '{printf "%s",length($0)}'`
        echo "Length of the supplied string is : $String_Length"
        if [ $? != 0 ]
        then
                 echo "Error. Command execution failed."
        else
                echo "Command executed successfully."
        fi
fi
