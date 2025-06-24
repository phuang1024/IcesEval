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

for key, value in DATA.items():
    print(f"{key}: {len(value)} matches")
for key, value in DATA_BY_YEAR.items():
    print(f"{key}: {len(value)} matches")
for key, value in DATA_BY_SEASON.items():
    print(f"{key}: {len(value)} matches")
print(f"All matches: {len(DATA_ALL)} matches")


# GPA vs rating
gpa_norate = []
gpa_excellent = []
gpa_outstanding = []
for entry in DATA_ALL:
    try:
        gpa = float(entry["WadeGPA"])
    except ValueError:
        continue
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
