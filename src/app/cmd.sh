#! /bin/bash
url=$1
dealay=$2
sleep $dealay
null=$(curl -s $url)
echo $url >> /app/debug.txt