"""
Match ICES data to catalog courses.
Edits json file from catalog.py
"""

import argparse
import json
import os
import re

from utils import *


def append_unknown_subj(subj):
    """
    Save subject to log file (if not already present).
    """
    if os.path.isfile("unknown_subjects.txt"):
        with open("unknown_subjects.txt", "r") as fp:
            subjects = fp.read().splitlines()
    else:
        subjects = []

    if subj not in subjects:
        subjects.append(subj)

    with open("unknown_subjects.txt", "w") as fp:
        fp.write("\n".join(subjects))


def parse_text(pdf_path):
    os.system(f"pdftotext -layout {pdf_path} /tmp/ices.txt")
    with open("/tmp/ices.txt", "r") as fp:
        lines = fp.readlines()

    with open("subjects.json", "r") as fp:
        subjects = json.load(fp)

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
            subject = search_subject(subjects, line)
            if subject is None:
                append_unknown_subj(line)
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

            courses = " ".join(words[i:])

            if subject is not None:
                yield (subject[0], first, last, courses, ta, outstanding)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_json")
    parser.add_argument("--out_json")
    parser.add_argument("--ices")
    args = parser.parse_args()

    with open(args.in_json, "r") as fp:
        data = json.load(fp)

    for rating in parse_text("ices.txt"):
        # Find matching course.
        for i in range(len(data)):
            entry = data[i]
            equal = True
            if not str_eq(entry["long_subject"], rating[0]):
                equal = False
            for first, last in entry["instructors"]:
                if str_eq(last, rating[2]):
                    break
            else:
                equal = False
            if not entry["course_num"] in rating[3]:
                equal = False

            if equal:
                data[i]["ices"] = {
                    "major": rating[0],
                    "first": rating[1],
                    "last": rating[2],
                    "courses": rating[3],
                    "ta": rating[4],
                    "outstanding": rating[5],
                }
                break

        else:
            print(f"Warning: No match for {rating[0]} {rating[1]} {rating[2]} {rating[3]}")

    with open(args.out_json, "w") as fp:
        json.dump(data, fp, indent=4)


if __name__ == "__main__":
    main()
