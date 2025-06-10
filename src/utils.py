import string


def str_eq(a, b):
    """
    String equality, ignoring case and whitespace.
    """
    return a.replace(" ", "").lower() == b.replace(" ", "").lower()


def str_in(a, b):
    """
    Check if string `a` is in string `b`, ignoring case, punctuation, and whitespace.
    """
    a = a.replace(" ", "").lower()
    a = a.translate(str.maketrans("", "", string.punctuation))
    b = b.replace(" ", "").lower()
    b = b.translate(str.maketrans("", "", string.punctuation))
    return a in b


def search_subject(subjects, query):
    """
    If query matches either abbreviation or full name,
    return the tuple (abbreviation, full name).
    """
    for subj in subjects:
        if str_in(subj[0], query) or str_in(subj[1], query) or str_in(query, subj[0]) or str_in(query, subj[1]):
            return subj
