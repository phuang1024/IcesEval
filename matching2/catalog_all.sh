#!/bin/bash

set -e

for year in {2010..2022}; do
    for season in fa sp; do
        python catalog.py --output ../data/catalog/catalog_${season}${year}.csv --season ${season} --year ${year} --force_restart > ../data/catalog/catalog_${season}${year}.log
    done
done
