#!/bin/bash

USER_HOME=$1
DESTINATION=$2
ARCHIVE_NAME="backup_$(date +'%Y%m%d%H%M%S').tar.gz"
LOGFILE="./logs/backup.log"

mkdir -p $DESTINATION

tar -czvf ${DESTINATION}/${ARCHIVE_NAME} ${USER_HOME} >> $LOGFILE 2>&1

echo "Backup completed and saved as $ARCHIVE_NAME on $(date)" >> $LOGFILE

cd $DESTINATION
ls -t | sed -e '1,${MAX_BACKUPS}d' | xargs -d '\n' rm -f
