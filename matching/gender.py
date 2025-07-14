"""
Use LLM to guess genders in graybook csv.

This operates on the output of graybook.py inplace.
"""

import argparse
import time

from google.genai import Client
from tqdm import tqdm

from utils import *

PROMPT_HEADER = """
In the following list of firstname, lastname, guess the gender of each person.
Do not change the order or exact spelling of names.
Output in CSV format with keys Last, First, Gender.
"""


def guess_gender(names, token):
    client = Client(api_key=token)

    prompt = PROMPT_HEADER
    for entry in names:
        prompt += f"{entry[0]}, {entry[1]}\n"
    prompt += "\n"

    r = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=prompt,
    )
    results = []
    for line in r.text.strip().split("\n"):
        if line.strip() == "Last,First,Gender":
            continue
        parts = line.strip().split(",")
        if len(parts) != 3:
            continue

        last = parts[0].strip()
        first = parts[1].strip().replace('"', '')

        gender = parts[2].strip().upper()
        if gender not in ("MALE", "FEMALE"):
            gender = "NONE"
        results.append((last, first, gender))

    assert len(results) == len(names)

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="CSV from graybook.py")
    parser.add_argument("--token", help="GoogleAI API token file.", required=True)
    parser.add_argument("--batch_size", type=int, default=150)
    args = parser.parse_args()

    with open(args.token, "r") as f:
        token = f.read().strip()

    while True:
        data = read_csv(args.file)

        # Get a set of unlabeled names.
        names = set()
        total_remain = 0
        for entry in data:
            if entry["Gender"] == "TODO":
                if len(names) < args.batch_size:
                    names.add((entry["Last"], entry["First"]))
                total_remain += 1

        if len(names) == 0:
            break

        print(f"Total remain: {total_remain}, batch size: {len(names)}")

        genders = guess_gender(names, token)

        # Update results.
        for i in range(len(data)):
            entry = data[i]
            if entry["Gender"] != "TODO":
                continue

            # Find corresponding in genders.
            gender = "NONE"
            for g in genders:
                if entry["Last"] == g["Last"] and entry["First"] == g["First"]:
                    gender = g["Gender"]
                    break

            if gender != "NONE":
                entry[i]["Gender"] = gender

        write_csv(args.file, data)

    print("Finished.")


if __name__ == "__main__":
    main()
