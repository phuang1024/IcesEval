"""
Catalog scraping utils.
"""

__all__ = (
    "get_xml",
    "search_for_obj",
)

from xml.etree import ElementTree

import requests

from subject import load_subjects

XML_CACHE = {}
BASE_URL = "https://courses.illinois.edu/cisapp/explorer/catalog/2024/fall.xml"


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


def find_course_sections(subject, course_num, term, last_name):
    """
    tree: Root XML.
    subject: ECE
    course_num: 220
    term: Fall 2024
    last_name: Asdf
    """
    base_xml = get_xml(BASE_URL)
    subject_xml = get_xml(search_for_obj(base_xml, "subjects", subject).attrib["href"])
    course_xml = get_xml(search_for_obj(subject_xml, "courses", course_num).attrib["href"])
    term_xml = get_xml(search_for_obj(course_xml, "termsOffered", term).attrib["href"])

    for obj in term_xml.find("sections"):
        section_xml = get_xml(obj.attrib["href"])
        for meeting in section_xml.find("meetings"):
            for instr in meeting.find("instructors"):
                if last_name in instr.attrib["lastName"].lower():
                    return section_xml

    return None
