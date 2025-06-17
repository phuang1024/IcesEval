#!/bin/bash

set -e

for year in 2014 2013 2012 2011 2010; do
    for season in fa sp; do
        echo "Processing term: ${season}${year}"
        python catalog.py --output ../data/catalog/catalog_${season}${year}.csv --season ${season} --year ${year} --force_restart > ../data/catalog/catalog_${season}${year}.log
    done
done
