#!/bin/sh
set -e
[[ $1 ]] && day=$1 || day=$(date +%d)

url=https://adventofcode.com/2022/day/$day
open $url

d=$(printf "%02d" $day)
mkdir -p $d
cd $d

[ -f main.py ] || cp ../aoc/template.py main.py
touch sample.txt

[[ ! -f input.txt && $AOC_SESSION ]] && \
    curl $url/input --cookie session=$AOC_SESSION -sS > input.txt

source $(poetry env info --path)/bin/activate
ls * | entr python main.py sample.txt -d
