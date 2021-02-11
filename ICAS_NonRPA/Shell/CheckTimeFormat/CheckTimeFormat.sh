:'
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'
#!/bin/sh

vTime="$1"

if [ $# -lt "1" ]
then
        echo "Error. Incorrect number of arguments passed to the script"
        exit 1
else
        while [ $# -gt 0 ];
        do
                case "$1" in
                        -vTime*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         vTime="${1#*=}"
                         ;;
                        -ProcessInstanceId*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         ProcessInstanceId="${1#*=}"
                         ;;

                esac
                shift
        done
fi

# Check if vTime is null
if [ -z "${vTime}" ]; then
     echo "CheckTimeFormat" "Time argument is null"
else
        # Split the colon out of vTime
        v_colon=`echo ${vTime} | awk '{printf "%s",substr($0 ,index($0,":"),1)}'`
                # Check for a colon
        if [ "${v_colon}" != ":" ]; then
                echo "Please enter the Time in HH:MM:SS or HH:MM Format"
        else
                # Split the hours out of vTime
                v_hours=`echo ${vTime} | awk '{printf "%s",substr($0 ,1,index($0,":")-1)}'`
                # Split the minutes out of vTime
                v_mins=`echo ${vTime} | awk '{printf "%s",substr($0,index($0,":")+1,2)}'`
                # Check if minutes is 2 character
                len=`expr ${v_mins} : '.*' `
                        if [ ${len} -ne 2 ]; then
                                echo "CheckTimeFormat : Minute is not in correct format"
                                        # Check the hours and minutes are in the correct ranges
                        elif [ ${v_hours} -lt 0 -o ${v_hours} -gt 23  -o ${v_mins} -gt 59 ]; then
                                                echo "CheckTimeFormat :Incorrect range for hour/mins in the format."
                        else
                                        echo "The Time Format entered is $vTime "
                                                if [ $? != 0 ]
                                                        then
                                                                echo "Error. Command execution failed."
                                                        else
                                                                echo "Command executed successfully."
                                                fi
                        fi
        fi
fi
