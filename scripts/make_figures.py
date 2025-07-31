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

COLLEGES = {}
for entry in read_csv("../data/colleges.csv"):
    COLLEGES[entry["Subject"]] = entry["College"]

COLLEGE_NAMES = {
    "LC": "Vet med",
    "KW": "General studies",
    "KM": "Business",
    "KU": "Law",
    "LL": "Social work",
    "KV": "LAS",
    "KR": "FAA",
    "LP": "Library and info sci",
    "KT": "Media",
    "KL": "Agriculture, consumer, env sciences",
    "KN": "Education",
    "KP": "Engineering",
    "KY": "Applied health sci",
    "LD": "?",
    "KS": "Graduate",
    "LG": "Labor and employment",
    "LT": "Media",
}


def get_data_by_rating():
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

    return gpa_norate, gpa_excellent, gpa_outstanding


def print_stats_by_rating():
    gpa_norate, gpa_excellent, gpa_outstanding = get_data_by_rating()

    def print_stats(data):
        print(f"  Count: {len(data)}")
        print(f"  Mean: {np.mean(data):.2f}")
        print(f"  Std Dev: {np.std(data):.2f}")

    print("No Rating:")
    print_stats(gpa_norate)
    print("Excellent Rating:")
    print_stats(gpa_excellent)
    print("Outstanding Rating:")
    print_stats(gpa_outstanding)
    print("Any rating (E + O):")
    print_stats(gpa_excellent + gpa_outstanding)
    print("All:")
    all_gpa = gpa_norate + gpa_excellent + gpa_outstanding
    print_stats(all_gpa)


# Sanity check: Rating frequency, separated by whether Wade entry exists.
def rating_freq_sanity_check():
    wade_total = 0
    wade_count = 0
    nowade_total = 0
    nowade_count = 0
    for entry in DATA_ALL:
        if entry["WadeGPA"] != "NONE":
            wade_total += 1
            if entry["ICESRating"] != "NONE":
                wade_count += 1
        else:
            nowade_total += 1
            if entry["ICESRating"] != "NONE":
                nowade_count += 1

    wade_freq = wade_count / wade_total if wade_total > 0 else 0
    nowade_freq = nowade_count / nowade_total if nowade_total > 0 else 0
    print(f"Wade entries: {wade_total} total, {wade_count} rated ({wade_freq:.2%})")
    print(f"No Wade entries: {nowade_total} total, {nowade_count} rated ({nowade_freq:.2%})")

    plt.clf()
    plt.bar(["Yes", "No"], [wade_freq, nowade_freq], color=['blue', 'orange'], alpha=0.7)
    plt.xlabel("GPA Data Exists?")
    plt.ylabel("Frequency")
    plt.title("Rating Frequency by GPA Data Status")
    plt.show()


def hist_gpa():
    all_gpa = [float(entry["WadeGPA"]) for entry in DATA_ALL if entry["WadeGPA"] != "NONE"]
    plt.clf()
    plt.hist(all_gpa, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    plt.xlabel("GPA")
    plt.ylabel("Frequency")
    plt.title("Distribution of GPA Values")
    plt.xlim(0, 4)
    plt.tight_layout()
    plt.show()


def plot_boxplot(data, labels, notch=True, label_medians=False, title="GPA Distribution by Professor Rating"):
    plt.clf()
    plt.figure(figsize=(10, 3))
    plt.boxplot(
        data,
        tick_labels=labels,
        orientation="horizontal",
        showfliers=False,
        notch=notch,
        widths=0.5,
    )

    # Label medians
    if label_medians:
        medians = [np.median(d) for d in data]
        for i, median in enumerate(medians):
            plt.text(median - 0.06, i + 1, f"{median:.2f}", ha='center', va='center', color='black')

    plt.xlabel("GPA")
    plt.title(title)
    plt.tight_layout()
    plt.show()


# GPA vs rating
def gpa_vs_rating():
    gpa_norate, gpa_excellent, gpa_outstanding = get_data_by_rating()
    gpa_rated = gpa_excellent + gpa_outstanding

    plot_boxplot(
        [gpa_norate, gpa_rated],
        labels=["No Rating", "Rated"]
    )
    plot_boxplot(
        [gpa_norate, gpa_excellent, gpa_outstanding],
        labels=["No Rating", "Excellent", "Outstanding"]
    )


# Same as above, more condensed.
def gpa_vs_rating_condensed():
    gpa_norate, gpa_excellent, gpa_outstanding = get_data_by_rating()
    gpa_rated = gpa_excellent + gpa_outstanding

    plot_boxplot(
        [gpa_norate, gpa_rated],
        labels=[f"No Rating ({len(gpa_norate)})", f"E/O Rating ({len(gpa_rated)})"],
        notch=False,
        label_medians=True,
        title="GPA Distribution by Professor Rating (Medians Labeled)"
    )


# GPA and rating frequency by college.
def stats_by_college():
    all_colleges = set()
    for entry in COLLEGES.values():
        all_colleges.add(entry)

    count = {s: 0 for s in all_colleges}
    rated = {s: 0 for s in all_colleges}
    gpa = {s: [] for s in all_colleges}
    for entry in DATA_ALL:
        if entry["Subject"] not in COLLEGES:
            continue
        coll = COLLEGES[entry["Subject"]]
        if entry["WadeGPA"] != "NONE":
            count[coll] += 1
            gpa[coll].append(float(entry["WadeGPA"]))
            if entry["ICESRating"] != "NONE":
                rated[coll] += 1

    # Sort subjects by rating frequency.
    freq = {s: rated[s] / count[s] if count[s] > 0 else 0 for s in all_colleges}
    sorted_subjects = sorted(freq, key=freq.get)

    # Sort by median GPA.
    medians = {s: np.median(gpa[s]) if gpa[s] else 0 for s in all_colleges}
    sorted_subjects = sorted(medians, key=medians.get)

    # Prepare data for plotting.
    data = []
    labels = []
    for i, s in enumerate(sorted_subjects):
        data.append(gpa[s])
        labels.append(f"{s} ({rated[s]}/{count[s]})")

    plt.clf()
    plt.figure(figsize=(12, 9))
    plt.boxplot(
        data,
        tick_labels=labels,
        orientation="horizontal",
        showfliers=False,
        widths=0.3,
    )
    # Annotate college names
    for i, subj in enumerate(sorted_subjects):
        plt.text(min(medians[subj], 3.5), i + 1.3, COLLEGE_NAMES[subj], ha='center', va='center', color='black')
    plt.xlabel("GPA")
    plt.xlim(0, 4)
    plt.title("GPA Distribution by Subject")
    #plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
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


def stats_by_gender():
    gpa_male = []
    gpa_female = []
    rated_male = 0
    rated_female = 0

    # Only entries with WadeGPA have gender data.
    for entry in DATA_ALL:
        if entry["WadeGPA"] == "NONE" or entry["Gender"] == "NONE":
            continue

        gpa = float(entry["WadeGPA"])
        rated = entry["ICESRating"] != "NONE"
        if entry["Gender"] == "MALE":
            gpa_male.append(gpa)
            if rated:
                rated_male += 1
        elif entry["Gender"] == "FEMALE":
            gpa_female.append(gpa)
            if rated:
                rated_female += 1
        else:
            raise ValueError(f"Unknown gender: {entry['Gender']}")

    # Plot GPA vs Gender
    plt.clf()
    plt.figure(figsize=(10, 4))
    plt.boxplot(
        [gpa_female, gpa_male],
        tick_labels=["Female", "Male"],
        orientation="horizontal",
        showfliers=False,
        notch=True,
        widths=0.4,
    )
    plt.xlabel("GPA")
    plt.title("GPA Distribution by Professor Gender")

    # Make another set of X axes, so we can plot the rating frequency.
    freq_male = rated_male / len(gpa_male)
    freq_female = rated_female / len(gpa_female)
    ax2 = plt.gca().twiny()
    ax2.barh([1, 2], [freq_female, freq_male], color='blue', alpha=0.3, height=0.3, label='Rating Frequency')
    ax2.set_xlabel("Rating Frequency")
    ax2.set_xlim(0, 1)

    plt.tight_layout()
    plt.show()


def compute_rpb(x, y):
    """
    Compute point biserial correlation.
    X: Negative values (no rating GPA).
    Y: Positive values (rated GPA).
    """
    n0 = len(x)
    n1 = len(y)
    n = n0 + n1
    m0 = np.mean(x)
    m1 = np.mean(y)
    s = np.std(x + y)

    return (m1 - m0) / s * np.sqrt(n0 * n1 / (n ** 2))


def corr_by_year():
    data_points = []

    for year, data in DATA_BY_YEAR.items():
        gpa_norate = []
        gpa_rate = []
        for entry in data:
            if entry["WadeGPA"] != "NONE":
                gpa = float(entry["WadeGPA"])
                if entry["ICESRating"] == "NONE":
                    gpa_norate.append(gpa)
                else:
                    gpa_rate.append(gpa)

        rpb = compute_rpb(gpa_norate, gpa_rate)
        data_points.append((year, rpb))

    plt.clf()
    plt.bar(
        [str(year) for year, _ in data_points],
        [rpb for _, rpb in data_points],
        color='skyblue', alpha=0.7
    )
    plt.xlabel("Year")
    plt.ylabel("Point-Biserial Correlation (rPB)")
    plt.xticks(rotation=45, ha='right')
    plt.title("rPB by Year")
    plt.tight_layout()
    plt.show()


corr_by_year()
