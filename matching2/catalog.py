"""
Catalog scraper.
Each run will scrape the entire catalog for one term.

Because this will take a while, the script saves it's state in a json file,
and can resume from where it left off, in case of failure.

XML tree:
Base -> Subject -> Course -> Term -> Section

Cache format:
- In Base, index of current subject.
- In Subject, index of current course.
- In Term, index of current section.
These indices are the *next* entry to scrape.
"""

import argparse
import json
import os
from xml.etree import ElementTree

import requests

from utils import *

CACHE_PATH = "catalog_cache.json"

XML_CACHE = {}


def get_xml(url, use_cache=True):
    """
    Section XMLs are not cached because they are numerous, and only used once.
    """
    if use_cache and url in XML_CACHE:
        return XML_CACHE[url]

    response = requests.get(url)
    response.raise_for_status()
    tree = ElementTree.fromstring(response.content)

    if use_cache:
        XML_CACHE[url] = tree

    return tree


def step(base_url, cache, year, season) -> dict:
    """
    Get the next section entry.

    Increment cache indices in place. Carry over as necessary.

    Returns data for the section:
        subject_code, course_num, instr_last, instr_first, crn
    """
    base_xml = get_xml(base_url)
    subjects = base_xml.find("subjects")

    subject_code = subjects[cache["subject_index"]].attrib["id"]
    subject_xml = get_xml(subjects[cache["subject_index"]].attrib["href"])
    courses = subject_xml.find("courses")

    course_num = courses[cache["course_index"]].attrib["id"]
    course_xml = get_xml(courses[cache["course_index"]].attrib["href"])
    sections = course_xml.find("sections")

    crn = sections[cache["section_index"]].attrib["id"]
    section_xml = get_xml(sections[cache["section_index"]].attrib["href"], use_cache=False)

    instructors = section_xml.find("meetings")[0].find("instructors")
    if len(instructors) == 0:
        instr_first = ""
        instr_last = ""
    else:
        # TODO assuming last instructor is primary.
        instr = instructors[-1]
        instr_first = instr.attrib["firstName"]
        instr_last = instr.attrib["lastName"]

    # Increment cache indices.
    cache["section_index"] += 1
    if cache["section_index"] >= len(sections):
        cache["section_index"] = 0
        cache["course_index"] += 1
        if cache["course_index"] >= len(courses):
            cache["course_index"] = 0
            cache["subject_index"] += 1

    return {
        "Subject": subject_code,
        "Course": course_num,
        "InstrLast": instr_last,
        "InstrFirst": instr_first,
        "CRN": crn,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Output CSV.")
    parser.add_argument("--year", required=True)
    parser.add_argument("--season", required=True, help="Short season name.")
    parser.add_argument("--force-restart", action="store_true")
    args = parser.parse_args()

    base_url = f"https://courses.illinois.edu/cisapp/explorer/schedule/{args.year}/{long_season_name(args.season)}.xml"
    print(f"Using base URL: {base_url}")

    # Load or initialize cache.
    if not os.path.isfile(CACHE_PATH) or args.force_restart:
        cache = {
            "subject_index": 0,
            "course_index": 0,
            "section_index": 0,
        }
    else:
        with open(CACHE_PATH, "r") as f:
            cache = json.load(f)
    print("Starting from state cache:", cache)

    # If output exists, print current length.
    if os.path.isfile(args.output):
        data = read_csv(args.output)
        print(f"Resuming to {args.output}. Current length: {len(data)}")

    # Get total number of subjects.
    num_subjects = len(get_xml(base_url).find("subjects"))

    while True:
        entry = step(base_url, cache, args.year, args.season)
        print(f"Scraped: {entry}")

        # Write to output CSV.
        if os.path.isfile(args.output):
            data = read_csv(args.output)
        else:
            data = []
        data.append(entry)
        write_csv(args.output, data)

        # Save cache.
        with open(CACHE_PATH, "w") as f:
            json.dump(cache, f, indent=4)

        # Check if done.
        if cache["subject_index"] >= num_subjects:
            print("Done.")
            break


if __name__ == "__main__":
    main()
