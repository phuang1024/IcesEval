"""
All subject abbreviations and names.

Main entry point: Scrape web page to get all subjects, and save to file.
"""

import json

from catalog import *

BASE_URL = "https://courses.illinois.edu/cisapp/explorer/schedule/2024/fall.xml"


def main():
    xml = get_xml(BASE_URL)
    subjects = []
    for obj in xml.find("subjects"):
        abbr = obj.attrib["id"]
        name = obj.text.strip()
        subjects.append((abbr, name))

    with open("subjects.json", "w") as fp:
        json.dump(subjects, fp, indent=4)


if __name__ == "__main__":
    main()
