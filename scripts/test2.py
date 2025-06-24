import random

import numpy as np

from utils import *


file = "../data/match/a.csv"
data = read_csv(file)

gpa_norate = []
gpa_rate = []
for entry in data:
    if entry["WadeGPA"]:
        if entry["ICESRating"] != "NONE":
            gpa_rate.append(float(entry["WadeGPA"]))
        else:
            gpa_norate.append(float(entry["WadeGPA"]))


print("No rating:")
print("n=", len(gpa_norate))
print("mean=", np.mean(gpa_norate))
print("std=", np.std(gpa_norate))

print("\nWith rating:")
print("n=", len(gpa_rate))
print("mean=", np.mean(gpa_rate))
print("std=", np.std(gpa_rate))
