"""
All subject abbreviations and names.

Main entry point: Scrape web page to get all subjects, and save to file.
"""

from dataclasses import dataclass

from catalog import *

BASE_URL = "https://courses.illinois.edu/cisapp/explorer/schedule/2024/fall.xml"


@dataclass
class Subject:
    abbr: str
    name: str


def get_subject(subjects: list[Subject], key: str) -> Subject:
    """
    Get subject by abbr or name.
    """
    key = key.strip().lower()
    for subject in subjects:
        if subject.abbr.lower() == key or subject.name.lower() == key:
            return subject
    raise ValueError(f"Subject {key} not found.")


def save_subjects(subjects: list[Subject], path: str):
    """
    Save subjects to a file.
    """
    with open(path, "w") as f:
        for subject in subjects:
            f.write(f"{subject.abbr}\t{subject.name}\n")


def load_subjects(path: str) -> list[Subject]:
    """
    Load subjects from a file.
    """
    subjects = []
    with open(path, "r") as f:
        for line in f:
            abbr, name = line.strip().split("\t")
            subjects.append(Subject(abbr=abbr, name=name))
    return subjects


def main():
    xml = get_xml(BASE_URL)
    subjects = []
    for obj in xml.find("subjects"):
        abbr = obj.attrib["id"]
        name = obj.text.strip()
        subjects.append(Subject(abbr=abbr, name=name))

    save_subjects(subjects, "subjects.txt")


if __name__ == "__main__":
    main()
