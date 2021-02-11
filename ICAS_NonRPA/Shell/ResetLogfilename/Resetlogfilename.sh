:'
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'
#!/bin/sh -x

if [ $# -lt 1 ]
then
        echo "Error. Incorrect number of arguments passed to the script"
        exit 1
else
        while [ $# -gt 0 ];
        do
                case "$1" in
                        -logDirectory*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         logDirectory="${1#*=}"
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

cd $logDirectory
for logfile in ${logDirectory}/*
do
        echo ${logfile}
        echo ${logDirectory}
        logname=`basename $logfile`
        log_datetime=`ls -altr ${logfile} | cut -d' ' -f6-8`
        datetime_string=`echo ${log_datetime} | sed -e 's/ /_/g'`
        filemod_date=`echo ${log_datetime} | cut -d' ' -f1-2 | sed -e 's/ /_/g'`
        currdate=`date | cut -d' ' -f2-3 | sed -e 's/ /_/g'`
        #echo "filemod -- $filemod_date"
        #echo "curr - $currdate"
        if [ "${filemod_date}" != "${currdate}" ]
        then
                new_logname="${logname}.old.${log_datetime}"
                mv "${logfile}" "${logDirectory}${logname}_${datetime_string}"
				                if [ $? -eq 0 ]
                then
                        touch ${logfile}
                        echo "Older logfile was renamed successfully"
                else
                        echo "move command failed"
                fi
        else
                        echo "Logfile in the log directory has current date of modification, hence no changes needed"
                fi
done
fi
