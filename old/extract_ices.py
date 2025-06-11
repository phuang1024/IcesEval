"""
Extract data from ICES data of excellent professors.
PDF to CSV.
"""

import argparse
import os
import re
from collections import namedtuple
from pathlib import Path
from tempfile import gettempdir

rating = namedtuple("Rating", ("major", "first", "last", "courses", "ta", "outstanding"))


def extract_pdf(path):
    tmp = Path(gettempdir()) / "ices.txt"
    os.system(f"pdftotext -layout {path} {tmp}")
    return tmp


def parse_text(text_path):
    with open(text_path, "r") as fp:
        lines = fp.readlines()

    start_i = 0
    while True:
        if start_i >= len(lines):
            raise ValueError("Reached end without finding start.")
        # TODO assumes first major is Accountancy.
        if lines[start_i].strip().lower() == "accountancy":
            break
        start_i += 1

    data = {}
    major = None
    for index in range(start_i, len(lines)):
        line = lines[index].replace(",", " ").strip().lower()
        if not line:
            continue
        words = line.split()

        # Skip page footer.
        if "spring" in words or "summer" in words or "fall" in words or "winter" in words:
            if re.search(r"\d\d\d\d", line):
                continue

        # Major.
        if not any(x.isdigit() for x in words):
            major = line
            print(f"Found major: {major}")
            continue

        # Professor.
        assert major is not None
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

            courses = " ".join(words[i:])

            # Add to data.
            if major not in data:
                data[major] = []
            data[major].append(rating(major, first, last, courses, ta, outstanding))

    return data


def write_csv(data, path):
    with open(path, "w") as fp:
        fp.write("major,first,last,courses,ta,outstanding\n")
        for major, ratings in data.items():
            for r in ratings:
                fp.write(f"{major},{r.first},{r.last},{r.courses},{r.ta},{r.outstanding}\n")


def parse_csv(path):
    data = []
    with open(path, "r") as fp:
        fp.readline()
        for line in fp:
            major, first, last, courses, ta, outstanding = line.strip().split(",")
            ta = ta.lower() == "true"
            outstanding = outstanding.lower() == "true"
            data.append(rating(major, first, last, courses, ta, outstanding))
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    text = extract_pdf(args.input)
    data = parse_text(text)
    write_csv(data, args.output)


if __name__ == "__main__":
    main()
