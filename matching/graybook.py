"""
Process list of names obtained from gray book.

Download CSV from Challen's CSV.
https://github.com/gchallen/graybooker

Run this file to parse relevant names and salaries.
"""

import argparse

from utils import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Raw CSV from Challen.")
    parser.add_argument("output", help="Output CSV.")
    args = parser.parse_args()

    data = []
    for entry in read_csv(args.input):
        if "prof" in entry["Title"].lower() and entry["Location"].strip() == "Urbana-Champaign Campus":
            last, first = entry["Name"].split(", ")
            last = last.strip().lower()
            first = first.strip().lower()

            data.append({
                "Last": last,
                "First": first,
                "Year": entry["Year"],
                "Salary": entry["PresentTotalSalary"],
                "Gender": "TODO",
            })

    write_csv(args.output, data)


if __name__ == "__main__":
    main()
