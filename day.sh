#!/bin/sh
set -e
[[ $1 ]] && day=$1 || day=$(date +%d)

d=$(printf "%02d" $day)
mkdir -p $d
cd $d

[ -f main.py ] || cp ../template.py main.py
touch sample.txt

[[ $AOC_SESSION ]] && curl -sS --cookie session=$AOC_SESSION \
    https://adventofcode.com/2022/day/$day/input > input.txt
