:'
Copyright 2020 Infosys Ltd.
Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at 
https://opensource.org/licenses/Apache-2.0 .
'
#!/bin/sh

if [ $# -lt "5" ]
then
        echo "Error. Incorrect number of arguments passed to the script"
        exit 1
else
        while [ $# -gt 0 ];
        do
                case "$1" in
                        -user*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         user="${1#*=}"
                         ;;
                        -remoteHost*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         remoteHost="${1#*=}"
                         ;;
                        -srcFilePath*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         srcFilePath="${1#*=}"
                         ;;
                        -remoteFilePath*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         remoteFilePath="${1#*=}"
                         ;;
                        -filename*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         filename="${1#*=}"
                         ;;
                        -ProcessInstanceId*)
                         if [[ "$1" != *=* ]]; then shift; fi
                         ProcessInstanceId="${1#*=}"
                         ;;
                        *)
                         echo "Error. Invalid argument passed"
                         exit 1
                         ;;
                esac
                shift
        done
fi
#echo "user is $user remoteHost is $remoteHost srcFilePath is $srcFilePath remoteFilePath is $remoteFilePath filename is $filename"
sftp ${user}@${remoteHost}:${remoteFilePath} <<- EOF
put ${srcFilePath}/${filename}
exit
EOF

if [ $? != 0 ]
then
        echo "Error. SFTP command execution failed."
else
        echo "SFTP command executed successfully."
fi