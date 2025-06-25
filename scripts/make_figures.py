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
    all_levels = (1, 2, 3, 4, 5)

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

    # Make another set of X axes, so we can plot the rating frequency.
    ax2 = plt.gca().twiny()
    rated_freq = [rated[level] / count[level] if count[level] > 0 else 0 for level in all_levels]
    ax2.barh(all_levels, rated_freq, color='blue', alpha=0.3, height=0.3, label='Rating Frequency')
    ax2.set_xlabel("Rating Frequency")
    ax2.set_xlim(0, 1)

    plt.show()

    # Make new figure: Scatterplot between GPA and frequency.
    plt.clf()
    x = [np.mean(gpa[level]) for level in all_levels]
    y = rated_freq
    labels = [f"{level}00s" for level in all_levels]
    plt.scatter(x, y, color='blue', alpha=0.7)
    for i, label in enumerate(labels):
        plt.annotate(label, (x[i], y[i]), textcoords="offset points", xytext=(0, 5), ha='center')
    plt.xlabel("Average GPA")
    plt.ylabel("Rating Frequency")
    plt.title("Average GPA vs Rating Frequency by Course Level")
    #plt.xlim(0, 4)
    #plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()


# Bar graph and histogram of rating frequency by GPA range.
def rating_freq_by_gpa():
    # Bar graph
    bins = 10
    rated_count = [0] * bins
    totals = [0] * bins

    for entry in DATA_ALL:
        if entry["WadeGPA"] == "NONE":
            continue

        gpa = float(entry["WadeGPA"])
        bin_index = int(gpa // (4.0 / bins))
        if bin_index >= bins:
            bin_index = bins - 1

        totals[bin_index] += 1
        if entry["ICESRating"] != "NONE":
            rated_count[bin_index] += 1

    freqs = [rated_count[i] / totals[i] if totals[i] > 0 else 0 for i in range(bins)]
    bin_labels = [f"{i * (4.0 / bins):.2f} - {(i + 1) * (4.0 / bins):.2f}" for i in range(bins)]

    plt.clf()
    plt.bar(bin_labels, freqs, color='skyblue', alpha=0.7)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("GPA Range")
    plt.ylabel("Rating Frequency")
    plt.title("Rating Frequency by GPA Range")
    plt.tight_layout()
    plt.show()

    # Histogram
    bins = 15

    all_values = []
    rated_values = []
    for entry in DATA_ALL:
        if entry["WadeGPA"] != "NONE":
            gpa = float(entry["WadeGPA"])
            all_values.append(gpa)
            if entry["ICESRating"] != "NONE":
                rated_values.append(gpa)

    plt.clf()
    plt.hist(all_values, bins=bins, alpha=0.5, label='All GPA Values', color='gray', edgecolor='black', density=True, range=(0, 4))
    plt.hist(rated_values, bins=bins, alpha=0.5, label='Rated GPA Values', color='lightblue', edgecolor='black', density=True, range=(0, 4))
    plt.xlabel("GPA")
    plt.ylabel("Frequency")
    plt.title("Frequency of GPA Values by Rating Status")
    plt.legend()
    plt.tight_layout()
    plt.show()


def stats_by_year():
    # 1. Average GPA by year.
    x = range(2010, 2023)
    y = []
    for year in x:
        gpas = [float(entry["WadeGPA"]) for entry in DATA_BY_YEAR[year] if entry["WadeGPA"] != "NONE"]
        if gpas:
            y.append(np.mean(gpas))
        else:
            y.append(0)

    plt.clf()
    plt.scatter(x, y, color='blue', alpha=0.7)
    plt.plot(x, y, color='blue', alpha=0.5)
    plt.xlabel("Year")
    plt.ylabel("Average GPA")
    plt.title("Average GPA by Year")
    plt.ylim(0, 4)
    plt.tight_layout()
    plt.show()

    # 2. Rating frequency by year.
    x = range(2010, 2023)
    totals = [0] * len(x)
    rated_counts = [0] * len(x)
    for i, year in enumerate(x):
        for entry in DATA_BY_YEAR[year]:
            if entry["WadeGPA"] != "NONE":
                totals[i] += 1
                if entry["ICESRating"] != "NONE":
                    rated_counts[i] += 1

    freqs = [rated_counts[i] / totals[i] if totals[i] > 0 else 0 for i in range(len(x))]

    plt.clf()
    plt.bar(x, freqs, color='skyblue', alpha=0.7)
    plt.xlabel("Year")
    plt.ylabel("Rating Frequency")
    plt.title("Rating Frequency by Year")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()


def stats_by_season():
    gpa_fall = []
    rated_fall = 0
    for entry in DATA_BY_SEASON["fa"]:
        if entry["WadeGPA"] != "NONE":
            gpa_fall.append(float(entry["WadeGPA"]))
            if entry["ICESRating"] != "NONE":
                rated_fall += 1

    gpa_spring = []
    rated_spring = 0
    for entry in DATA_BY_SEASON["sp"]:
        if entry["WadeGPA"] != "NONE":
            gpa_spring.append(float(entry["WadeGPA"]))
            if entry["ICESRating"] != "NONE":
                rated_spring += 1

    freq_fall = rated_fall / len(gpa_fall) if gpa_fall else 0
    freq_spring = rated_spring / len(gpa_spring) if gpa_spring else 0

    # Superimpose box plot of GPA, and bar graph of rating frequency.
    plt.clf()
    plt.figure(figsize=(10, 4))
    plt.boxplot(
        [gpa_fall, gpa_spring],
        tick_labels=["Fall", "Spring"],
        orientation="horizontal",
        showfliers=False,
        notch=True,
        widths=0.4,
    )
    plt.xlabel("GPA")
    plt.title("GPA Distribution by Season")

    # Make another set of X axes, so we can plot the rating frequency.
    ax2 = plt.gca().twiny()
    ax2.barh([1, 2], [freq_fall, freq_spring], color='blue', alpha=0.3, height=0.3, label='Rating Frequency')
    ax2.set_xlabel("Rating Frequency")
    ax2.set_xlim(0, 1)

    plt.tight_layout()
    plt.show()


stats_by_year()
