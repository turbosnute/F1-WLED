#! /bin/bash
url=$1
delay=$2
sleep $delay
null=$(curl -s $url)
echo $url >> /app/debug.txt
