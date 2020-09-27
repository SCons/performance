#!/bin/bash

python profile_run.py 1 $1
python time_run.py 1 $1
python time_run.py 2 $1
python time_run.py 3 $1
python memwatch_run.py 1 $1
python eval_all.py $1

