"""
Verify between our ICES parsing, and Wade's ICES parsing.
"""

from utils import *


our_path = "../data/ices/ices_fa2022.csv"
wade_path = "../data/wades_tre/tre-fa2022.csv"

our_data = read_csv(our_path)
wade_data = read_csv(wade_path)


print("Read data:")
print(f"  OurData ({our_path}): {len(our_data)} entries")
print(f"  WadeData ({wade_path}): {len(wade_data)} entries")
print()


not_found = []
for i, our_entry in enumerate(our_data):
    found = False
    classes = our_entry["Courses"].split(";")
    for wade_entry in wade_data:
        if wade_entry["fname"].lower() == our_entry["InstrFirst"]:
            if wade_entry["lname"].lower() == our_entry["InstrLast"]:
                if wade_entry["course"] in classes:
                    found = True
                    break
    if not found:
        not_found.append(i)

print(f"Matching OurData to WadeData:")
print(f"  {len(not_found)} entries not found in WadeData")
print(f"  Indices:")
print("    " + ", ".join(map(str, not_found)))
print()
