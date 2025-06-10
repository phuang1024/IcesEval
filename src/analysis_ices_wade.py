import json

import matplotlib.pyplot as plt


# Helper functions

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


def z_test(population, sample):
    pop_mean = sum(population) / len(population)
    pop_std = (sum((x - pop_mean) ** 2 for x in population) / len(population)) ** 0.5
    sample_mean = sum(sample) / len(sample)
    std_error = pop_std / (len(sample) ** 0.5)
    z = (sample_mean - pop_mean) / std_error
    print("Z test:")
    print(f"Pop size: {len(population)}")
    print(f"Pop mean: {pop_mean}")
    print(f"Pop std: {pop_std}")
    print(f"Sample size: {len(sample)}")
    print(f"Sample mean: {sample_mean}")
    print(f"Standard error: {std_error}")
    print(f"Z: {z}")


with open("wade_ices_matched.json", "r") as fp:
    data = json.load(fp)


def z_test_gpa():
    # Get all numerical data.
    population = []
    rated = []
    for item in data:
        population.append(float(item["Average Grade"]))
        if item["ICES"] != "NONE":
            rated.append(float(item["Average Grade"]))

    plot_hists(
        ("Population", population),
        ("Rated", rated),
    )
    z_test(population, rated)


def histogram_gpa():
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


def gpa_by_course_level():
    population = []
    one = []
    two = []
    three = []
    four = []
    five = []
    for item in data:
        population.append(float(item["Average Grade"]))
        assert len(item["Course"]) == 3
        level = item["Course"][0]
        match level:
            case "1":
                one.append(float(item["Average Grade"]))
            case "2":
                two.append(float(item["Average Grade"]))
            case "3":
                three.append(float(item["Average Grade"]))
            case "4":
                four.append(float(item["Average Grade"]))
            case "5":
                five.append(float(item["Average Grade"]))
            case _:
                print("Warning: Unknown course:", item["Course"])

    plot_hists(
        ("Population", population),
        ("100s", one),
        ("200s", two),
        ("300s", three),
        ("400s", four),
        ("500s", five),
    )
    print("100s z test:")
    z_test(population, one)
    print("200s z test:")
    z_test(population, two)
    print("300s z test:")
    z_test(population, three)
    print("400s z test:")
    z_test(population, four)
    print("500s z test:")
    z_test(population, five)


gpa_by_course_level()
