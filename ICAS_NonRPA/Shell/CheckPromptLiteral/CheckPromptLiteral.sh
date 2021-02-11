:'
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'
#!/bin/sh

if [ $# -lt 1 ]
then
        echo "Error: Incorrect number of arguments passed to the script"
        exit 1
else
        while [ $# -gt 0 ];
                do
                case "$1" in
                        -user1*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         user1="${1#*=}"
                         ;;
                        -user2**)
                         if [[ "$1" != *=* ]]; then shift; fi
                         user2="${1#*=}"
                         ;;
                        -user3**)
                         if [[ "$1" != *=* ]]; then shift; fi
                         user3="${1#*=}"
                         ;;
                        -user4**)
                         if [[ "$1" != *=* ]]; then shift; fi
                         user4="${1#*=}"
                         ;;
                        -ProcessInstanceId*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         ProcessInstanceId="${1#*=}"
                         ;;
                esac
                shift
        done
                if [[ "$user1" == "$user2" || "$user1" == "$user3" || "$user1" == "$user4" ]]; then

                        PromptLiteral=`echo $user1 | tr a-z A-Z`
                        echo "successful"
                else

                        echo "failed"

                fi
