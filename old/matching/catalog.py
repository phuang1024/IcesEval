"""
Get all courses from catalog.
"""

import json
import time
from xml.etree import ElementTree

import requests
from tqdm import tqdm

BASE_URL = "https://courses.illinois.edu/cisapp/explorer/catalog/2022/fall.xml"


def get_xml(url):
    response = requests.get(url)
    response.raise_for_status()
    tree = ElementTree.fromstring(response.content)
    return tree


def search_for_obj(tree, element: str, text: str):
    """
    Inside tree/<element>, search for element that contains text
    in id or content.
    """
    text = text.lower()
    for obj in tree.find(element):
        if text == obj.attrib.get("id", "").lower() or text == obj.text.lower():
            return obj
    return None


def extract_term(url):
    parts = url.split("/")
    year, season = parts[-2], parts[-1]
    season = season.split(".")[0]
    return f"{season} {year}"


def main():
    all_courses = []
    term = extract_term(BASE_URL)

    base_xml = get_xml(BASE_URL)
    count = 0
    for subj in (pbar := tqdm(base_xml.find("subjects"))):
        # Iterate all subjects.
        abbr = subj.attrib["id"]
        pbar.set_description(abbr)
        long_subj = subj.text
        for course in get_xml(subj.attrib["href"]).find("courses"):
            # Iterate all courses.
            course_num = course.attrib["id"]
            course_name = course.text
            for term_obj in get_xml(course.attrib["href"]).find("termsOffered"):
                # Find correct term.
                if term_obj.text.lower().replace(" ", "") != term.lower().replace(" ", ""):
                    continue
                for section in get_xml(term_obj.attrib["href"]).find("sections"):
                    # Iterate all sections.
                    try:
                        section_xml = get_xml(section.attrib["href"])
                        instructors = []
                        for meeting in section_xml.find("meetings"):
                            for instr in meeting.find("instructors"):
                                instructors.append((
                                    instr.attrib["firstName"],
                                    instr.attrib["lastName"],
                                ))
                        all_courses.append({
                            "subject": abbr,
                            "long_subject": long_subj,
                            "course_num": course_num,
                            "course_name": course_name,
                            "term": term,
                            "section_id": section.attrib["id"],
                            "instructors": instructors,
                        })
                        count += 1

                    except Exception as e:
                        print(f"Error: subj={abbr}, course={course_num}, section={section.attrib['id']}.")
                        print(f"Exception: {e}")

                    # Save every iteration.
                    with open("catalog.json", "w") as fp:
                        json.dump(all_courses, fp, indent=4)


if __name__ == "__main__":
    main()
