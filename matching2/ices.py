"""
Parse and match ICES data.

ICES data is much more sparse than Wade (as it's meant to be human readable).
It contains: A list of professors ranked "excellent".
    Professors are identified with their name, subject (long subject name), and course number(s).

To match this data, we parse the downloaded PDF file.
We look for a heading that looks like a subject name; then assume that every line after is
a professor belonging to that subject.

First, for verification purposes, we parse the ICES file into a CSV.
Then we match it to the catalog data with subject, name, and course number.
"""

import argparse
import os
import re
import string

from catalog import get_xml
from utils import *


def get_subjects():
    """
    Using the FA24 page, get a list of subjects and their abbreviations.
    """
    url = "https://courses.illinois.edu/cisapp/explorer/schedule/2024/fall.xml"
    xml = get_xml(url)
    subjects = []
    for obj in xml.find("subjects"):
        abbr = obj.attrib["id"]
        name = obj.text.strip()
        subjects.append((abbr, name))

    return subjects


def parse_ices(pdf_path):
    subjects = get_subjects()

    os.system(f"pdftotext -layout {pdf_path} /tmp/ices.txt")
    with open("/tmp/ices.txt", "r") as fp:
        lines = fp.readlines()

    start_i = 0
    while True:
        if start_i >= len(lines):
            raise ValueError("Reached end without finding start.")
        # TODO assumes first subject is Accountancy.
        if lines[start_i].strip().lower() == "accountancy":
            break
        start_i += 1

    subject = None
    for index in range(start_i, len(lines)):
        line = lines[index].replace(",", " ").strip().lower()
        if not line:
            continue
        words = line.split()

        # Skip page footer.
        if "spring" in words or "summer" in words or "fall" in words or "winter" in words:
            if re.search(r"\d\d\d\d", line):
                continue

        # Subject
        if not any(x.isdigit() for x in words):
            for subject in subjects:
                line = line.lower().translate(str.maketrans("", "", string.punctuation + " "))
                name = subject[1].lower().translate(str.maketrans("", "", string.punctuation + " "))
                if line in name or name in line:
                    break
            else:
                subject = None
                print("Unknown subject:", line)

            continue

        # Professor.
        if len(words) >= 3:
            i = 0
            outstanding = words[0] == "*"
            if outstanding:
                i += 1

            for j in range(i, len(words)):
                if words[j] == "ta" or words[j].isdigit():
                    break
            first = words[j - 1]
            last = " ".join(words[i:j - 1])
            i = j

            ta = words[i] == "ta"
            if ta:
                i += 1

            courses = ";".join(words[i:])

            if subject is not None:
                yield {
                    "Subject": subject[0],
                    "InstrFirst": first,
                    "InstrLast": last,
                    "TA": ta,
                    "Courses": courses,
                    "Outstanding": outstanding,
                }


def match_to_ices(ices_entry, catalog_data) -> dict | None:
    """
    Find entry in catalog that matches given ICES entry.
    """
    courses = ices_entry["Courses"].split(";")

    for catalog_entry in catalog_data:
        if catalog_entry["Subject"] == ices_entry["Subject"]:
            if catalog_entry["Course"] in courses:
                if match_all_instructors(
                        (ices_entry["InstrFirst"], ices_entry["InstrLast"]),
                        parse_instructors(catalog_entry["Instructors"])):
                    return catalog_entry

    return None


def main():
    parser = argparse.ArgumentParser()
    subp = parser.add_subparsers(dest="command")

    conv_p = subp.add_parser("convert", help="Convert ICES PDF to CSV.")
    conv_p.add_argument("-i", "--input", required=True, help="Input ICES PDF file.")
    conv_p.add_argument("-o", "--output", required=True, help="Output CSV file.")

    verify_p = subp.add_parser("verify", help="Verify ICES CSV against catalog data.")
    verify_p.add_argument("--ices", required=True, help="Input ICES CSV file.")
    verify_p.add_argument("--catalog", required=True, help="Input catalog CSV file.")

    args = parser.parse_args()

    if args.command == "convert":
        write_csv(args.output, list(parse_ices(args.input)))

    else:
        ices_data = read_csv(args.ices)
        catalog_data = read_csv(args.catalog)

        print("Matching catalog and ICES.")

        # Stats variables.
        no_match = 0
        matched = 0

        for ices_entry in ices_data:
            match = match_to_ices(ices_entry, catalog_data)
            if match is None:
                print("No match for ICES entry:", ices_entry)
                no_match += 1
            else:
                matched += 1

        print("Stats (matching Wade to catalog):")
        print(f"  Total ICES entries: {len(ices_data)}")
        print(f"  Total catalog entries: {len(catalog_data)}")
        print(f"  No match: {no_match}")
        print(f"  Matched: {matched}")


if __name__ == "__main__":
    main()
