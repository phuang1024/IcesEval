#!/bin/bash

# Run match.py on all terms.

mkdir -p ../data/match

for year in {2010..2022}; do
    for season in fa sp; do
        echo Processing ${season}${year}
        python match.py --catalog ../data/catalog/catalog_${season}${year}.csv \
            --ices ../data/ices/ices_${season}${year}.csv \
            --wade ../data/wade/wade_${season}${year}.csv \
            --graybook ../data/graybook/nodups.csv \
            --year ${year} \
            --output ../data/match/match_${season}${year}.csv \
            > ../data/match/match_${season}${year}.log 2>&1 || echo "  Error!"
    done
done
