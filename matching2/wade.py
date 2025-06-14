import argparse

from utils import *


def parse_wade(file):
    ret = []
    for entry in read_csv(file):
        # Keys change across years.
        for key in entry.keys():
            if key.lower().strip() in ("subject", "course subject"):
                subj_key = key
            elif key.lower().strip() in ("course", "course number"):
                course_key = key

        names = entry["Primary Instructor"].lower().split(", ")
        if len(names) == 2:
            last, first = names
            last = last.strip().lower()
            first = first.strip()[0].lower()
        else:
            last = ""
            first = ""

        ret.append({
            "Subject": entry[subj_key],
            "Course": entry[course_key],
            "InstrLast": last,
            "InstrFirst": first,
            "CRN": entry["CRN"],
            "GPA": entry["Average Grade"],
        })

    return ret


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Input Wade CSV.")
    parser.add_argument("--catalog", required=True, help="Input catalog CSV.")
    args = parser.parse_args()

    wade_data = parse_wade(args.input)
    catalog_data = read_csv(args.catalog)

    print("Matching catalog and Wade.")

    # Stats variables.
    no_match = 0
    attrs_wrong = 0
    matched = 0

    for wade_entry in wade_data:
        # Match by CRN
        for catalog_entry in catalog_data:
            if wade_entry["CRN"] == catalog_entry["CRN"]:
                break
        else:
            print("No match for Wade entry:", wade_entry)
            no_match += 1
            continue

        # Verify all attributes.
        if (wade_entry["Subject"] == catalog_entry["Subject"]
                and wade_entry["Course"] == catalog_entry["Course"]
                and wade_entry["InstrLast"].lower() == catalog_entry["InstrLast"].lower()
                and wade_entry["InstrFirst"].lower() == catalog_entry["InstrFirst"].lower()):
            matched += 1
        else:
            print("Attributes mismatch for Wade entry:", wade_entry)
            print("    Catalog entry:                 ", catalog_entry)
            attrs_wrong += 1

    print("Stats (matching Wade to catalog):")
    print(f"  Total Wade entries: {len(wade_data)}")
    print(f"  Total catalog entries: {len(catalog_data)}")
    print(f"  No match: {no_match}")
    print(f"  Attributes mismatch: {attrs_wrong}")
    print(f"  Matched: {matched}")


if __name__ == "__main__":
    main()
