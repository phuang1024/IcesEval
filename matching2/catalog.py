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

Instructors format:
First1,Last1;First2,Last2;
"""

import argparse
import json
import os
from threading import Thread
from xml.etree import ElementTree

import requests

from utils import *

CACHE_PATH = "catalog_cache.json"

XML_CACHE = {}


def get_xml(url, use_cache=True):
    """
    Section XMLs are not cached because they are numerous, and only used once.
    """
    # Fix occasional problems with URLs.
    if "cis.local" in url:
        url = url.replace("cis.local", "courses.illinois.edu")
        url = url.replace("cisapi", "cisapp/explorer")
        url = url + ".xml"

    if use_cache and url in XML_CACHE:
        return XML_CACHE[url]

    response = requests.get(url)
    response.raise_for_status()
    tree = ElementTree.fromstring(response.content)

    if use_cache:
        XML_CACHE[url] = tree

    return tree


def step_section(rets, i, section_tag, subject_code, course_num) -> dict:
    crn = section_tag.attrib["id"]
    section_xml = get_xml(section_tag.attrib["href"], use_cache=False)

    instr_string = ""
    for instr in section_xml.find("meetings")[0].find("instructors"):
        instr_string += instr.attrib["firstName"] + "," + instr.attrib["lastName"] + ";"

    rets[i] = {
        "Subject": subject_code,
        "Course": course_num,
        "Instructors": instr_string,
        "CRN": crn,
    }


def step(base_url, cache) -> list[dict]:
    """
    Get the next section entry.

    Increment cache indices in place. Carry over as necessary.

    Returns data for the section:
        subject_code, course_num, instr_last, instr_first, crn
    OR returns None, if there was an error.
    """
    base_xml = get_xml(base_url)
    subjects = base_xml.find("subjects")

    subject_code = subjects[cache["subject_index"]].attrib["id"]
    subject_xml = get_xml(subjects[cache["subject_index"]].attrib["href"])
    courses = subject_xml.find("courses")

    course_num = courses[cache["course_index"]].attrib["id"]
    course_xml = get_xml(courses[cache["course_index"]].attrib["href"])
    sections = course_xml.find("sections")

    threads = []
    rets = [None] * len(sections)
    for i in range(len(sections)):
        thread = Thread(target=step_section, args=(rets, i, sections[i], subject_code, course_num))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    # Increment cache indices.
    cache["section_index"] = 0
    cache["course_index"] += 1
    if cache["course_index"] >= len(courses):
        cache["course_index"] = 0
        cache["subject_index"] += 1

    return rets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Output CSV.")
    parser.add_argument("--year", required=True)
    parser.add_argument("--season", required=True, help="Short season name.")
    parser.add_argument("--force_restart", action="store_true")
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
    else:
        data = []

    # Get total number of subjects.
    num_subjects = len(get_xml(base_url).find("subjects"))

    while True:
        entries = step(base_url, cache)
        for e in entries:
            print(f"Scraped: {e}", flush=True)

        # Write to output CSV.
        data.extend(entries)
        write_csv(args.output, data)

        # Save cache.
        with open(CACHE_PATH, "w") as f:
            json.dump(cache, f, indent=4)

        # Check if done.
        if cache["subject_index"] >= num_subjects:
            print("Done.", flush=True)
            break


if __name__ == "__main__":
    main()
