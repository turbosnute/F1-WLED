#!/bin/bash

DEPLOYPATH=`python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])'`/fastf1/livetiming/clientmod2.py
mv clientmod2.py $DEPLOYPATH
