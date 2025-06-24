import random

from utils import *


file = "../data/match/a.csv"
data = read_csv(file)

yes_wade_indices = []
no_wade_indices = []
for i, entry in enumerate(data):
    if entry["WadeGPA"]:
        yes_wade_indices.append(i)
    else:
        no_wade_indices.append(i)


yes = random.sample(yes_wade_indices, 20)
no = random.sample(no_wade_indices, 20)

print("Yes Wade:")
for i in yes:
    print("  ", i, data[i])
print("\nNo Wade:")
for i in no:
    print("  ", i, data[i])
