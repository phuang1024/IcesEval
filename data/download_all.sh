#!/bin/bash

set -e

# Download all ICES and Wade datasets.

function down() {
    wget $1 -O $2
}

ICES=http://citl.illinois.edu/docs/default-source/teachers-ranked-as-excellent/
WADE=https://raw.githubusercontent.com/wadefagen/datasets/refs/heads/main/gpa/raw/

function download_ices() {
    mkdir -p ices
    cd ices

    down ${ICES}tre-2024-fall.pdf   ices_fa2024.pdf
    down ${ICES}tre-2024-spring.pdf ices_sp2024.pdf
    down ${ICES}tre-2023-fall.pdf   ices_fa2023.pdf
    down ${ICES}tre-2023-spring.pdf ices_sp2023.pdf
    down ${ICES}tre-2022-fall.pdf   ices_fa2022.pdf
    down ${ICES}tre-2022-spring.pdf ices_sp2022.pdf
    down ${ICES}tre-2021-fall.pdf   ices_fa2021.pdf
    down ${ICES}tre-2021-spring.pdf ices_sp2021.pdf
    down ${ICES}tre-2020-fall.pdf   ices_fa2020.pdf
    down ${ICES}tre-2020-spring.pdf ices_sp2020.pdf
    down ${ICES}tre-2019-fall.pdf   ices_fa2019.pdf
    down ${ICES}tre-2019-spring.pdf ices_sp2019.pdf
    down ${ICES}tre-2018-fall.pdf   ices_fa2018.pdf
    down ${ICES}tre-2018-spring.pdf ices_sp2018.pdf
    down ${ICES}tre-2017-fall.pdf   ices_fa2017.pdf
    down ${ICES}tre-2017-spring.pdf ices_sp2017.pdf
    down ${ICES}tre-2016-fall.pdf   ices_fa2016.pdf
    down ${ICES}tre-2016-spring.pdf ices_sp2016.pdf
    down ${ICES}fall15list.pdf      ices_fa2015.pdf
    down ${ICES}spring15list.pdf    ices_sp2015.pdf
    down ${ICES}fall14list.pdf      ices_fa2014.pdf
    down ${ICES}spring14list.pdf    ices_sp2014.pdf
    down ${ICES}fall13list.pdf      ices_fa2013.pdf
    down ${ICES}spring13list.pdf    ices_sp2013.pdf
    down https://citl.illinois.edu/docs/default-source/default-document-library/fall2012list.pdf?sfvrsn=0  ices_fa2012.pdf
    down ${ICES}spring12list.pdf    ices_sp2012.pdf
    down https://citl.illinois.edu/docs/default-source/ices-documents/lists-of-teachers-ranked-as-excellent/fall2011list.pdf?sfvrsn=2  ices_fa2011.pdf
    down ${ICES}spring11list.pdf    ices_sp2011.pdf
    down https://citl.illinois.edu/docs/default-source/ices-documents/lists-of-teachers-ranked-as-excellent/fall10list.pdf?sfvrsn=2  ices_fa2010.pdf
    down ${ICES}spring10list.pdf    ices_sp2010.pdf

    cd ..
}

function download_wade() {
    mkdir -p wade
    cd wade

    down ${WADE}fa2024.csv wade_fa2024.csv
    down ${WADE}sp2024.csv wade_sp2024.csv
    down ${WADE}fa2023.csv wade_fa2023.csv
    down ${WADE}sp2023.csv wade_sp2023.csv
    down ${WADE}fa2022.csv wade_fa2022.csv
    down ${WADE}sp2022.csv wade_sp2022.csv
    down ${WADE}fa2021.csv wade_fa2021.csv
    down ${WADE}sp2021.csv wade_sp2021.csv
    down ${WADE}fa2020.csv wade_fa2020.csv
    down ${WADE}sp2020.csv wade_sp2020.csv
    down ${WADE}fa2019.csv wade_fa2019.csv
    down ${WADE}sp2019.csv wade_sp2019.csv
    down ${WADE}fa2018.csv wade_fa2018.csv
    down ${WADE}sp2018.csv wade_sp2018.csv
    down ${WADE}fa2017.csv wade_fa2017.csv
    down ${WADE}sp2017.csv wade_sp2017.csv
    down ${WADE}fa2016.csv wade_fa2016.csv
    down ${WADE}sp2016.csv wade_sp2016.csv
    down ${WADE}fa2015.csv wade_fa2015.csv
    down ${WADE}sp2015.csv wade_sp2015.csv
    down ${WADE}fa2014.csv wade_fa2014.csv
    down ${WADE}sp2014.csv wade_sp2014.csv
    down ${WADE}fa2013.csv wade_fa2013.csv
    down ${WADE}sp2013.csv wade_sp2013.csv
    down ${WADE}fa2012.csv wade_fa2012.csv
    down ${WADE}sp2012.csv wade_sp2012.csv
    down ${WADE}fa2011.csv wade_fa2011.csv
    down ${WADE}sp2011.csv wade_sp2011.csv
    down ${WADE}fa2010.csv wade_fa2010.csv
    down ${WADE}sp2010.csv wade_sp2010.csv

    cd ..
}

function clean_wade() {
    cd wade
    for f in *.csv; do
        echo "Cleaning $f"
        iconv -f utf-8 -t utf-8 -c $f > /tmp/a.csv || true
        mv /tmp/a.csv $f
    done
    cd ..
}


download_ices
download_wade
clean_wade
