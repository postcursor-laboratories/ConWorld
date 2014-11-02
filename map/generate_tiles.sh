#!/bin/bash

# A thing to generate tiles in a certain range

lowx="$1"
highx="$2"
lowy="$3"
highy="$4"

echo "Generating from X=[$lowx,$highx], Y=[$lowy,$highy]"

for (( i=$lowx; $i<=$highx; i=$[$i+1] )); do
    for (( j=$lowy; $j<=$highy; j=$[$j+1] )); do
	./mapgen.py $i $j &
    done
done
