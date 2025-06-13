import json
import os


def read_data():
    data = {}
    for file in os.listdir("../data"):
        if file.endswith(".json"):
            parts = file.split(".")[0].split("_")
            year, season = parts[1], parts[2]
            with open(os.path.join("../data", file), "r") as fp:
                data[(year, season)] = json.load(fp)

    return data


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
