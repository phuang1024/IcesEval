#!/bin/bash

set -e

for year in {2010..2022}; do
    for term in fa sp; do
        python match_ices_wade.py --ices ../data/ices_${term}${year}.pdf --wade ../data/wade_${term}${year}.csv -o ../data/matched_${term}${year}.json
    done
done
