#!/bin/bash
set -e

[[ $1 ]] && day=$1 || day=$(date +%-d)
year=$(date +%Y)

dest=$year/$(printf "%02d" $day)
mkdir -p $dest
cd $dest

[ -f main.py ] || cp ../../aoc/template.py main.py
touch sample.txt

url=https://adventofcode.com/$year/day/$day
[[ ! -f input.txt && $AOC_SESSION ]] && \
    open $url && curl $url/input --cookie session=$AOC_SESSION -sS > input.txt

source $(poetry env info --path)/bin/activate
ls * | entr python main.py sample.txt -d
