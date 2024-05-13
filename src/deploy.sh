#!/bin/bash

DEPLOYPATH=`python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])'`/fastf1/livetiming/clientmod.py
mv clientmod.py $DEPLOYPATH
