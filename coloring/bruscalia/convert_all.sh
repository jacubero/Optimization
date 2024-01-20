#!/bin/bash

for file in $(ls ../data/gc*)
do
  filename="$(basename "$file")"
  python3 convert.py $file > $filename.txt
done
