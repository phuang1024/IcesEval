import csv


def long_season_name(s):
    if s == "fa":
        return "fall"
    elif s == "sp":
        return "spring"
    raise ValueError(f"Unknown season: {s}")


def short_season_name(s):
    if s == "fall":
        return "fa"
    elif s == "spring":
        return "sp"
    raise ValueError(f"Unknown season: {s}")


def write_csv(file, data: list[dict]):
    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def read_csv(file) -> list[dict]:
    with open(file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
