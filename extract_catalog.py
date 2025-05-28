"""
Webscraper for UIUC catalog.
https://courses.illinois.edu/cisdocs/explorer
"""

import argparse
from xml.etree import ElementTree

import requests
from tqdm import tqdm

from extract_ices import parse_csv

XML_CACHE = {}


def get_xml(url, use_cache=True):
    if use_cache and url in XML_CACHE:
        return XML_CACHE[url]
    response = requests.get(url)
    response.raise_for_status()
    tree = ElementTree.fromstring(response.content)
    if use_cache:
        XML_CACHE[url] = tree
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


def find_course_section(tree, subject, course_num, term, last_name):
    """
    tree: Root XML.
    subject: ECE
    course_num: 220
    term: Fall 2024
    last_name: Asdf
    """
    subject_xml = get_xml(search_for_obj(tree, "subjects", subject).attrib["href"])
    course_xml = get_xml(search_for_obj(subject_xml, "courses", course_num).attrib["href"])
    term_xml = get_xml(search_for_obj(course_xml, "termsOffered", term).attrib["href"])

    # Need to iterate through all sections.
    last_name = last_name.lower()
    for obj in term_xml.find("sections"):
        section_xml = get_xml(obj.attrib["href"])
        for meeting in section_xml.find("meetings"):
            for instr in meeting.find("instructors"):
                if last_name in instr.attrib["lastName"].lower():
                    return section_xml

    return None


def extract_term(url):
    parts = url.split("/")
    year, season = parts[-2], parts[-1]
    season = season.split(".")[0]
    return f"{season} {year}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_url", help="Include year and term.", default="https://courses.illinois.edu/cisapp/explorer/catalog/2024/fall.xml")
    parser.add_argument("--ices_data", help="Path to ICES CSV.")
    args = parser.parse_args()

    term = extract_term(args.base_url)
    print("Parsed term:", term)

    tree = get_xml(args.base_url)

    # Verify ICES data is accurate.
    data = parse_csv(args.ices_data)
    pbar = tqdm(total=len(data), desc="Verifying ICES data")
    for r in data:
        pbar.update(1)
        pbar.set_description(f"{r.major}: {r.first}. {r.last}")

        for course in r.courses.split():
            section = find_course_section(tree, r.major, course, term, r.last)
            if section is None:
                print(f"Warning: Could not find section for {r}, course={course}")


if __name__ == "__main__":
    main()
