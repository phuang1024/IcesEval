"""
Parse and match Wade dataset.

Wade dataset contains CRNs, so they can be unambiguously matched to catalog.
We still check the other attributes (instructor, course number).

Running this file will only print stats.
Use "matching.py" to generate the output matched file.
"""

import argparse

from utils import *


def parse_wade(file):
    ret = []
    for entry in read_csv(file):
        # Keys change across years.
        for key in entry.keys():
            name = key.strip("\ufeff").strip().lower()
            if name in ("subject", "course subject"):
                subj_key = key
            elif name in ("course", "course number"):
                course_key = key

        names = entry["Primary Instructor"].lower().split(", ")
        if len(names) == 2:
            last, first = names
            last = last.strip().lower()
            first = first.strip()[0].lower()
        else:
            last = ""
            first = ""

        #print(entry.keys())
        ret.append({
            "Subject": entry[subj_key],
            "Course": entry[course_key],
            "InstrLast": last,
            "InstrFirst": first,
            "CRN": entry["CRN"],
            "GPA": entry["Average Grade"],
        })

    return ret


def match_to_wade(wade_entry, catalog_data):
    """
    Find entry in catalog that matches given wade entry.

    returns (bool, bool, int):
        First (bool) is whether a match was found by CRN.
        Second (bool) is whether all attributes match (if first is true).
        Third is the index of catalog entry, or None, depending on if match was found via CRN.
    """
    # Match by CRN
    for i, catalog_entry in enumerate(catalog_data):
        if wade_entry["CRN"] == catalog_entry["CRN"]:
            break
    else:
        return False, False, None

    # Verify all attributes.
    attr_match = False
    if (wade_entry["Subject"] == catalog_entry["Subject"]
            and wade_entry["Course"] == catalog_entry["Course"]):
        if match_all_instructors(
                (wade_entry["InstrFirst"], wade_entry["InstrLast"]),
                parse_instructors(catalog_entry["Instructors"])):
            attr_match = True

    return True, attr_match, i


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wade", required=True, help="Input Wade CSV.")
    parser.add_argument("--catalog", required=True, help="Input catalog CSV.")
    args = parser.parse_args()

    wade_data = parse_wade(args.wade)
    catalog_data = read_csv(args.catalog)

    print("Matching catalog and Wade.")

    # Stats variables.
    no_match = 0
    attrs_wrong = 0
    matched = 0

    for wade_entry in wade_data:
        match, attr_match, index = match_to_wade(wade_entry, catalog_data)
        if not match:
            print("No match for Wade entry:", wade_entry)
            no_match += 1
        elif not attr_match:
            print("Attributes mismatch for Wade entry:", wade_entry)
            print("    Catalog entry:                 ", catalog_data[index])
            attrs_wrong += 1
        else:
            matched += 1

    print("Stats (matching Wade to catalog):")
    print(f"  Total Wade entries: {len(wade_data)}")
    print(f"  Total catalog entries: {len(catalog_data)}")
    print(f"  No match: {no_match}")
    print(f"  Attributes mismatch: {attrs_wrong}")
    print(f"  Matched: {matched}")


if __name__ == "__main__":
    main()
