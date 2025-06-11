import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    with open(args.input, "r") as infile, open(args.output, "w") as outfile:
        infile.readline()
        outfile.write("major,first,last,courses,ta,outstanding\n")
        for line in infile:
            values = line.strip().split(",")
            major = values[3].lower()
            first = values[-1].strip().lower()
            last = values[-2].strip().lower()
            course = values[1]
            print(f"Processing: {major}, {first}, {last}, {course}")

            outfile.write(f"{major},{first[0]},{last},{course},False,False\n")


if __name__ == "__main__":
    main()
