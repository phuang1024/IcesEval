#!/bin/bash

# Convert all ICES pdfs to csv.

set -e

for year in {2010..2022}; do
    for season in fa sp; do
        echo Processing ICES ${season}${year}
        python ices.py convert -i ../data/ices/ices_${season}${year}.pdf -o ../data/ices/ices_${season}${year}.csv > ../data/ices/ices_${season}${year}.log
    done
done
