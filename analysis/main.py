from utils import *

data = read_data()


def sep_by_season():
    # [number of ratings, total]
    fall = [0, 0]
    spring = [0, 0]

    for (year, season), ratings in data.items():
        for entry in ratings:
            if entry["ICES"] != "NONE":
                if season == "fall":
                    fall[0] += 1
                else:
                    spring[0] += 1
            if season == "fall":
                fall[1] += 1
            else:
                spring[1] += 1

    def print_stats(rated, total):
        print(f"Total: {total}")
        print(f"With rating: {rated}")
        print(f"Percentage: {rated / total * 100:.2f}%")
    print("FALL:")
    print_stats(fall[0], fall[1])
    print("SPRING:")
    print_stats(spring[0], spring[1])


sep_by_season()
