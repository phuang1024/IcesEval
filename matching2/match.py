"""
Match catalog, Wade, and ICES into a single CSV.

Matching is based on catalog;
any Wade or ICES entries not found in catalog are omitted.
"""

import argparse

from ices import match_to_ices
from utils import *
from wade import parse_wade, match_to_wade


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True, help="Catalog csv")
    parser.add_argument("--ices", required=True, help="ICES csv")
    parser.add_argument("--wade", required=True, help="Wade csv")
    parser.add_argument("-o", "--output", required=True, help="Output csv file")
    args = parser.parse_args()

    # Print file paths.
    print("Matching:")
    print("  Catalog:", args.catalog)
    print("  ICES:", args.ices)
    print("  Wade:", args.wade)
    print("  Output:", args.output)
    print()

    # Print catalog stats.
    catalog = read_csv(args.catalog)
    print("Catalog:")
    print(f"  Total entries: {len(catalog)}")
    print()

    # Match Wade.
    wade = parse_wade(args.wade)
    not_matched = []
    for i, wade_entry in enumerate(wade):
        match, _, catalog_i = match_to_wade(wade_entry, catalog)
        if match:
            catalog[catalog_i]["WadeGPA"] = wade_entry["GPA"]
        else:
            not_matched.append(i)

    # Print Wade stats.
    print("Wade:")
    print(f"  Total entries: {len(wade)}")
    print(f"  Matched: {len(wade) - len(not_matched)}")
    print(f"  Not matched: {len(not_matched)}")
    print(f"    Not matched indices in Wade:")
    print(f"      ", " ".join(map(str, not_matched)), sep="")
    print()

    # Match ICES.
    # First, initialize ICESRating field.
    for entry in catalog:
        entry["ICESRating"] = "NONE"
    ices = read_csv(args.ices)
    not_matched = []
    # ICES entries that have no corresponding Wade entry.
    no_wade = []
    for i, ices_entry in enumerate(ices):
        match = match_to_ices(ices_entry, catalog)
        if len(match) > 0:
            has_wade = False
            for catalog_i in match:
                catalog[catalog_i]["ICESRating"] = "OUTSTANDING" if ices_entry["Outstanding"] == "True" else "EXCELLENT"
                catalog[catalog_i]["ICESTA"] = ices_entry["TA"]
                if "WadeGPA" in catalog[catalog_i]:
                    has_wade = True
            if not has_wade:
                no_wade.append(i)

        else:
            not_matched.append(i)

    # Print ICES stats.
    print("ICES:")
    print(f"  Total entries: {len(ices)}")
    print(f"  Matched: {len(ices) - len(not_matched)}")
    print(f"  Not matched: {len(not_matched)}")
    print(f"    Not matched indices in ICES:")
    print(f"      ", " ".join(map(str, not_matched)), sep="")
    print(f"  No matching Wade entry: {len(no_wade)}")
    print(f"    No matching Wade indices in ICES:")
    print(f"      ", " ".join(map(str, no_wade)), sep="")
    print()

    # Compute intersection stats.
    nothing = 0
    only_ices = 0
    only_wade = 0
    both = 0
    for entry in catalog:
        ices_rated = entry["ICESRating"] != "NONE"
        if not ices_rated and "WadeGPA" not in entry:
            nothing += 1
        elif ices_rated and "WadeGPA" not in entry:
            only_ices += 1
        elif not ices_rated and "WadeGPA" in entry:
            only_wade += 1
        else:
            both += 1

    print("Coverage stats:")
    print("  Total catalog entries:", len(catalog))
    print("  Nothing matched:", nothing)
    print("  Only ICES matched:", only_ices)
    print("  Only Wade matched:", only_wade)
    print("  Both matched:", both)
    print()

    # Write output.
    print("Writing output to", args.output)
    # Make fieldnames.
    fieldnames = set(catalog[0].keys())
    fieldnames.add("ICESRating")
    fieldnames.add("ICESTA")
    fieldnames.add("WadeGPA")
    write_csv(args.output, catalog, fieldnames=list(fieldnames))


if __name__ == "__main__":
    main()
