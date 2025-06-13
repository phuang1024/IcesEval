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
