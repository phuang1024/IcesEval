def str_eq(a, b):
    """
    String equality, ignoring case and whitespace.
    """
    return a.replace(" ", "").lower() == b.replace(" ", "").lower()
