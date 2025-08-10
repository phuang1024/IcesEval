#!/bin/bash

set -e

for year in {2010..2024}; do
    for season in fa sp; do
        echo "Processing term: ${season}${year}"
        python catalog.py --output ../data/catalog/catalog_${season}${year}.csv --season ${season} --year ${year} --force_restart > ../data/catalog/catalog_${season}${year}.log
    done
done
