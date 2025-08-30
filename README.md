# Correlation between GPA and faculty evaluations at UIUC

Course grades and student evaluations of teaching are factors important for the career of students and professors respectively.
When faculty evaluations are determined by students, the integrity of the system can be compromised, because these are desirable measures mutually given to each other.
We use novel data of the University of Illinois Urbana-Champaign, and find a statistically significant positive correlation between GPA and teaching evaluations, and compute the strength of correlation in different departments.

Paper: https://github.com/phuang1024/IcesEval/blob/master/paper.pdf

Supplemental material: https://github.com/phuang1024/IcesEval/blob/master/supplement.pdf

Data: https://github.com/phuang1024/IcesEval/blob/master/data/

## Data format

We provide the "matched" data (`data/match/*.csv`) by year and semester.

Fall 2017 is missing because GPA data does not contain CRN.

Keys:

- Catalog keys: From catalog, covers all courses.
    - CRN: Course registration number (unique identifier).
    - Subject: E.g. "MATH", "CS", "HIST"
    - Course: E.g. "101", "241", "104"
    - Instructors: List of instructors for the section. First initial and full last name.
      Instructors separated by semicolon, and first and last names separated by comma.
- WadeGPA keys: From GPA dataset. Coverage varies.
    - WadeGPA: GPA of the section.
    - WadeInstrFirst: First initial (as from GPA dataset).
    - WadeInstrLast: Last name.
- ICES keys: From ICES "teachers ranked as excellent". Coverage varies.
    - ICESTA: Whether individual is a Teaching Assistant.
      If False, the individual is a professor.
    - ICESRating: "EXCELLENT", "OUTSTANDING", or "NONE".
- Graybook keys: From Graybook. Coverage varies.
    - GrayInstrFirst: Full first name of instructor.
    - Gender: Gender, guessed by LLM from first name. May be unreliable.
    - Salary: Salary of instructor.

## Scraping and matching

First, download ICES and WadeGPA data:

```bash
cd data
./download_all.sh
```

Download all catalog data.
Note: This will take a while (on the order of hours per term), and will send on the order
of 100K requests to `courses.illinois.edu`.

```bash
cd matching
./catalog_all.sh
```

Scraping can be resumed if interrupted, but the correct arguments must be given to the Python
file (term and year). Simply running `./catalog_all.sh` again will start over all terms.

Parse ICES data.

```bash
cd matching
./ices_all.sh
```

Match all data.

```bash
cd matching
./match_all.sh
```
