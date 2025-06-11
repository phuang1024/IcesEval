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
    parser.add_argument("--ices")
    parser.add_argument("--wade")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()

    ices_data = list(parse_text(args.ices))
    with open(args.wade, "r", newline="") as fp:
        wade_data = list(csv.DictReader(fp))

    for entry in tqdm(wade_data):
        entry["ICES"] = "NONE"
        entry["TA"] = False

        # Name in Wade
        names = entry["Primary Instructor"].lower().split(", ")
        if len(names) == 2:
            last, first = names
        else:
            print("Unexpected name format:", entry["Primary Instructor"])
            continue

        for rating in ices_data:
            if (
                entry["Subject"].lower() == rating[0].lower()
                and first[0] == rating[1].lower()
                and last == rating[2].lower()
                and entry["Course"] in rating[3]
            ):
                entry["ICES"] = "OUTSTANDING" if rating[5] else "EXCELLENT"
                entry["TA"] = rating[4]
                break

    with open(args.output, "w") as fp:
        json.dump(wade_data, fp, indent=2)


if __name__ == "__main__":
    main()
