#!/bin/bash

CONFIGS_PATH=$1
RUNS=100
LIBS=$(pwd)

cd $CONFIGS_PATH
python3 "${LIBS}/standard.py" -t -r $RUNS -c "conf_standard.json"
python3 "${LIBS}/self_adaptation.py" -t -r $RUNS -c "conf_adaptation.json"