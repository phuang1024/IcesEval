Version 2 of scripts to combine catalog, ICES, and Wade.

Catalog scraper:
Uses the tree of XML files to find all sections offered in a term.
Contains attributes: Subject, course, instructor name, CRN.

ICES parser:
Parses PDF document.
Contains: Subject, course, instructor name, ICES rating.
    Any instructor not in this list has no ICES rating.

Wade parser:
Parses Wade CSV data.
Contains: Subject, course, instructor name, CRN, GPA, number of students.

Matching script:
Combines catalog, ICES, and Wade data.
Generates an output CSV file which is the union of all three datasets.
    Because the catalog will be complete, this output should be the same length as the catalog.
Each entry will have additional attributes, if available:
    ICES rating.
    GPA.
    Enrollment.
