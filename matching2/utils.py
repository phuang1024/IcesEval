import csv
import string


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


def parse_instructors(s: str) -> list[tuple[str, str]]:
    """
    a,b;c,d;... -> [("a", "b"), ("c", "d"), ...]
    """
    instrs = []
    for instr in s.split(";"):
        if "," in instr:
            first, last = instr.strip().split(",", 1)
            instrs.append((first.strip(), last.strip()))
    return instrs


def match_instructor(instr1: tuple[str, str], instr2: tuple[str, str]) -> int:
    """
    Check if the given query matches any of the instructors,
    using a variety of string checking methods in case of data errors.

    NOTE: Naturally, this may make mistakes.

    Return:
    2: Exact match:
        First initials match, and one last name is in the other, and both last names are > 6 chars.
    1: Approx match:
        One last name is in the other.
        Regardless of first initial, or last name length.
    0: No match.
    """
    first1 = instr1[0].strip().lower()
    last1 = instr1[1].strip().lower()
    first2 = instr2[0].strip().lower()
    last2 = instr2[1].strip().lower()

    # Remove punctuation and spaces.
    last1_clean = last1.translate(str.maketrans("", "", string.punctuation + " "))
    last2_clean = last2.translate(str.maketrans("", "", string.punctuation + " "))

    # Check exact match.
    if first1 == first2:
        if len(last1) > 6 and len(last2) > 6:
            if last1_clean in last2_clean or last2_clean in last1_clean:
                return 2

    # Check approximate match.
    if last1_clean in last2_clean or last2_clean in last1_clean:
        return 1

    return 0


def match_all_instructors(query: tuple[str, str], instructors: list[tuple[str, str]]) -> list[int]:
    """
    Uses `match_instructor` to attempt to match all given instructors.

    Only instructors with the highest nonzero match score are returned.
        I.e. if there exists an instructor with a score of 2, only instructors with match score 2 are returned.
        If there are only match scores of zero, an empty list is returned.

    Return: Indices of `instructors` for best matches.
    """
    ones = []
    twos = []
    for i, instr in enumerate(instructors):
        match = match_instructor(query, instr)
        if match == 1:
            ones.append(i)
        elif match == 2:
            twos.append(i)

    if twos:
        return twos
    if ones:
        return ones
    return []
