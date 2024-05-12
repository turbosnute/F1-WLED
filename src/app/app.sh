#!/bin/bash

while :
do
  date
  echo "--- Start F1-WLED App"
  python3 /app/f1wled.py
  RET=$?
  if [ ${RET} -ne 0 ];
  then
    echo "Exit status not 0"
    echo "Sleep 120"
    sleep 120
  fi
  date
  echo "Sleep 60"
  sleep 60
done
