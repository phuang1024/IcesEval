"""
Parse and process list of names obtained from gray book.

Download CSV from Challen's CSV.
https://github.com/gchallen/graybooker

Run this file to parse relevant names, and guess gender with LLM.

match.py will read the resulting CSV file.
"""

import argparse
import os
import time

from tqdm import tqdm

from utils import *

PROMPT_HEADER = """
In the following list of firstname, lastname, guess the gender of each person.
Do not change the order or exact spelling of names.
Output in CSV format with keys Last, First, Gender.
"""


def guess_gender(names: list[dict], token: str, batch_size: int = 200, backoff: float = 2) -> list[dict]:
    from google.genai import Client
    client = Client(api_key=token)

    results = []

    i = 0
    pbar = tqdm(total=len(names), desc="Guessing gender")
    while True:
        if i >= len(names):
            break
        curr_names = names[i:i + batch_size]

        prompt = PROMPT_HEADER
        for entry in curr_names:
            prompt += f"{entry['Last']}, {entry['First']}\n"
        prompt += "\n"

        r = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )
        batch_results = []
        for line in r.text.strip().split("\n"):
            if line.strip() == "Last,First,Gender":
                continue
            parts = line.strip().split(",")
            if len(parts) != 3:
                continue

            gender = parts[2].strip().upper()
            if gender not in ("MALE", "FEMALE"):
                gender = "NONE"
            batch_results.append((parts[0].strip(), parts[1].strip(), gender))

        # Verify results.
        batch_good = True
        if len(batch_results) != len(curr_names):
            batch_good = False
        else:
            for i in range(len(curr_names)):
                if curr_names[i]["Last"] != batch_results[i][0] or curr_names[i]["First"] != batch_results[i][1]:
                    print("NO MATCH", curr_names[i], batch_results[i])
                    batch_good = False
                    break

        if not batch_good:
            print("Bad batch, i =", i)
        else:
            for res in batch_results:
                results.append({
                    "Last": res[0],
                    "First": res[1],
                    "Gender": res[2],
                })

            pbar.update(len(curr_names))

        i += batch_size
        time.sleep(backoff)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Raw CSV from Challen.")
    parser.add_argument("output", help="Output CSV.")
    parser.add_argument("--token", help="GoogleAI API token file.", required=True)
    args = parser.parse_args()

    with open(args.token, "r") as f:
        token = f.read().strip()

    # Index names by (year, first, last). Data is whatever other relevant data.
    data = {}
    for entry in read_csv(args.input):
        if "prof" in entry["Title"].lower() and entry["Location"].strip() == "Urbana-Champaign Campus":
            last, first = entry["Name"].split(", ")
            last = last.strip()
            first = first.strip()

            year = int(entry["Year"])

            data[(year, last, first)] = {
                "Salary": entry["PresentTotalSalary"],
            }

    # Get a list (set) of names.
    names = set()
    for (year, last, first), entry in data.items():
        names.add((last, first))
    names = [{"Last": last, "First": first} for last, first in names]

    genders = guess_gender(names, token)

    # Combine results.
    final_data = []
    for entry in data:
        year, last, first = entry
        salary = data[entry]["Salary"]

        # Find corresponding in genders.
        gender = "NONE"
        for g in genders:
            if last == g["Last"] and first == g["First"]:
                gender = g["Gender"]
                break

        final_data.append({
            "Last": last,
            "First": first,
            "Year": year,
            "Salary": salary,
            "Gender": gender,
        })

    # Write to output CSV.
    write_csv(args.output, final_data)


if __name__ == "__main__":
    main()
