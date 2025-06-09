import json

import matplotlib.pyplot as plt


def print_stats(data):
    print(f"Count: {len(data)}")
    print(f"Average: {sum(data) / len(data)}")


def plot_hists(*data, bins=10):
    """
    each data should be (name, list)
    """
    for name, d in data:
        print(f"Statistics for {name}:")
        print_stats(d)

    plt.clf()
    for name, d in data:
        plt.hist(d, bins=bins, alpha=0.5, label=name, density=True)
    plt.legend()
    plt.show()


with open("wade_ices_matched.json", "r") as fp:
    data = json.load(fp)

# Histogram of GPA separated by none, excellent, outstanding.
none = []
excellent = []
outstanding = []
for item in data:
    if item["ICES"] == "NONE":
        none.append(float(item["Average Grade"]))
    elif item["ICES"] == "EXCELLENT":
        excellent.append(float(item["Average Grade"]))
    elif item["ICES"] == "OUTSTANDING":
        outstanding.append(float(item["Average Grade"]))

plot_hists(
    ("None", none),
    ("Excellent", excellent),
    ("Outstanding", outstanding),
)

# Histogram of excellent/outstanding separated by TA.
ta_yes = [0, 0]
ta_no = [0, 0]
for item in data:
    lst = ta_yes if item["TA"] else ta_no
    if item["ICES"] == "NONE":
        lst[1] += 1
    else:
        lst[0] += 1

print(f"TA Yes: {ta_yes[0]} E/O, {ta_yes[1]} no rating.")
print(f"TA No: {ta_no[0]} E/O, {ta_no[1]} no rating.")
