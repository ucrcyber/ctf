#!/bin/bash
for i in $(seq -f "%02g" 50 -1 0)
        do
                unzip -P pass $i.zip
                #i=$((i-1))
        done
cat flag.txt