"""
Scrape a list of (subject, college) pairs.
"""

import argparse

from tqdm import tqdm

from catalog import get_xml
from utils import *


BASE_URL = "https://courses.illinois.edu/cisapp/explorer/catalog/2024/fall.xml"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", required=True, help="Output CSV file.")
    args = parser.parse_args()

    xml = get_xml(BASE_URL)

    results = []
    for sub in tqdm(xml.find("subjects")):
        sub_code = sub.attrib["id"]
        sub_url = sub.attrib["href"]
        sub_xml = get_xml(sub_url)
        college = sub_xml.find("collegeCode").text.strip()

        results.append({
            "Subject": sub_code,
            "College": college,
        })

    write_csv(args.output, results)


if __name__ == "__main__":
    main()
