import os
import random

import matplotlib.pyplot as plt
import numpy as np

from utils import *

# Load all data, indexed by various methods.
DATA = {}
DATA_BY_YEAR = {}
DATA_BY_SEASON = {}
DATA_ALL = []

for year in range(2010, 2023):
    for season in ("fa", "sp"):
        path = f"../data/match/match_{season}{year}.csv"
        if os.path.isfile(path):
            DATA[(year, season)] = read_csv(f"../data/match/match_{season}{year}.csv")
        else:
            print(f"File not found: {path}")
            DATA[(year, season)] = []
for year in range(2010, 2023):
    DATA_BY_YEAR[year] = DATA[(year, "fa")] + DATA[(year, "sp")]
for season in ("fa", "sp"):
    DATA_BY_SEASON[season] = []
    for year in range(2010, 2023):
        DATA_BY_SEASON[season] += DATA[(year, season)]
for year in range(2010, 2023):
    DATA_ALL += DATA_BY_YEAR[year]

if False:
    for key, value in DATA.items():
        print(f"{key}: {len(value)} matches")
    for key, value in DATA_BY_YEAR.items():
        print(f"{key}: {len(value)} matches")
    for key, value in DATA_BY_SEASON.items():
        print(f"{key}: {len(value)} matches")
    print(f"All matches: {len(DATA_ALL)} matches")


# GPA vs rating
def gpa_vs_rating():
    gpa_norate = []
    gpa_excellent = []
    gpa_outstanding = []
    for entry in DATA_ALL:
        if entry["WadeGPA"] != "NONE":
            gpa = float(entry["WadeGPA"])
            if entry["ICESRating"] == "NONE":
                gpa_norate.append(gpa)
            elif entry["ICESRating"] == "EXCELLENT":
                gpa_excellent.append(gpa)
            elif entry["ICESRating"] == "OUTSTANDING":
                gpa_outstanding.append(gpa)

    gpa_rated = gpa_excellent + gpa_outstanding

    def plot_boxplot(data, labels):
        plt.clf()
        plt.figure(figsize=(10, 3))
        plt.boxplot(
            data,
            tick_labels=labels,
            orientation="horizontal",
            showfliers=False,
            notch=True,
            widths=0.5,
        )
        plt.xlabel("GPA")
        plt.title("GPA Distribution by ICES Rating")
        plt.show()

    plot_boxplot(
        [gpa_norate, gpa_rated],
        labels=["No Rating", "Rated"]
    )
    plot_boxplot(
        [gpa_norate, gpa_excellent, gpa_outstanding],
        labels=["No Rating", "Excellent", "Outstanding"]
    )


# GPA and rating frequency by subject.
def stats_by_subject():
    all_subjects = set()
    for entry in DATA_ALL:
        all_subjects.add(entry["Subject"])

    count = {s: 0 for s in all_subjects}
    rated = {s: 0 for s in all_subjects}
    gpa = {s: [] for s in all_subjects}
    for entry in DATA_ALL:
        s = entry["Subject"]
        if entry["WadeGPA"] != "NONE":
            count[s] += 1
            gpa[s].append(float(entry["WadeGPA"]))
            if entry["ICESRating"] != "NONE":
                rated[s] += 1

    # Sort subjects by rating frequency.
    freq = {s: rated[s] / count[s] if count[s] > 0 else 0 for s in all_subjects}
    sorted_subjects = sorted(freq, key=freq.get, reverse=True)

    # Prepare data for plotting.
    data = []
    labels = []
    for i, s in enumerate(sorted_subjects):
        data.append(gpa[s])
        labels.append(f"{s} ({rated[s]}/{count[s]})")
        if i > 10:
            break

    plt.clf()
    plt.figure(figsize=(12, 6))
    plt.boxplot(
        data,
        tick_labels=labels,
        orientation="horizontal",
        showfliers=False,
        widths=0.3,
    )
    plt.xlabel("GPA")
    plt.title("GPA Distribution by Subject")
    #plt.xticks(rotation=45, ha='right')
    #plt.tight_layout()
    plt.show()


# GPA and rating frequency by level.
def stats_by_level():
    all_levels = (1, 2, 3, 4)

    count = {s: 0 for s in all_levels}
    rated = {s: 0 for s in all_levels}
    gpa = {s: [] for s in all_levels}
    for entry in DATA_ALL:
        level = entry["Course"][0]
        if not level.isdigit():
            continue
        level = int(level)
        if level not in all_levels:
            continue

        if entry["WadeGPA"] != "NONE":
            count[level] += 1
            gpa[level].append(float(entry["WadeGPA"]))
            if entry["ICESRating"] != "NONE":
                rated[level] += 1

    # Prepare data for plotting.
    data = []
    labels = []
    for level in all_levels:
        data.append(gpa[level])
        labels.append(f"{level}00s ({rated[level]}/{count[level]})")

    plt.clf()
    plt.figure(figsize=(12, 6))
    plt.boxplot(
        data,
        tick_labels=labels,
        orientation="horizontal",
        showfliers=False,
        notch=True,
        widths=0.4,
    )
    plt.xlabel("GPA")
    plt.title("GPA Distribution by Course Level")
    plt.show()

    # Make another plot of frequency of rated by level.
    rated_freq = [rated[level] / count[level] if count[level] > 0 else 0 for level in all_levels]
    plt.clf()
    plt.figure(figsize=(8, 4))
    plt.bar(all_levels, rated_freq, color='skyblue')
    plt.xticks(all_levels)
    plt.xlabel("Course Level")
    plt.ylabel("Rating Frequency")
    plt.title("E/O Rating Frequency by Course Level")
    plt.show()


stats_by_level()
