#!/bin/bash

python profile_run.py 1 $1 fast
python time_run.py 1 $1 fast
python eval_all.py $1

