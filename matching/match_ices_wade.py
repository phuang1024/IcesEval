"""
Match ICES and Wade datasets.
"""

import argparse
import csv
import json

from tqdm import tqdm

from ices import parse_text
from utils import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ices", required=True)
    parser.add_argument("--wade", required=True)
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--logfile")
    args = parser.parse_args()

    ices_data = list(parse_text(args.ices))
    with open(args.wade, "r", newline="") as fp:
        wade_data = list(csv.DictReader(fp))

    for entry in wade_data:
        entry["ICES"] = "NONE"
        entry["TA"] = False

        # Name in Wade
        names = entry["Primary Instructor"].lower().split(", ")
        if len(names) == 2:
            last, first = names
        else:
            print("Unexpected name format:", entry["Primary Instructor"])
            continue

        # Wade attributes
        subj_key = None
        course_key = None
        for key in entry.keys():
            if "subject" in key.lower():
                subj_key = key
            elif "course" in key.lower():
                course_key = key
        assert subj_key is not None
        assert course_key is not None
        subject = entry[subj_key].lower()
        course = entry[course_key].lower()

        for rating in ices_data:
            if (
                subject == rating[0].lower()
                and first[0] == rating[1].lower()
                and last == rating[2].lower()
                and course in rating[3]
            ):
                entry["ICES"] = "OUTSTANDING" if rating[5] else "EXCELLENT"
                entry["TA"] = rating[4]
                break

    with open(args.output, "w") as fp:
        json.dump(wade_data, fp, indent=2)


if __name__ == "__main__":
    main()
