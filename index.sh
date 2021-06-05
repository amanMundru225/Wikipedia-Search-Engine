#!/usr/bin/env bash
python3 2019201029/KWayMerge.py
python3 2019201029/BuildBlockDict.py
python3 2019201029/PreProcess.py
python3 2019201029/xmlParser.py
python3 2019201029/main.py ${1} ${2} ${3}

