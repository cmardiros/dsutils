def dict_to_code(mapping):
    """
    Convert input dict `mapping` to a string containing python code.

    Each key is the name of a variable and each value is
    the variable content. Each variable assignment is separated by
    a newline.

    Keys must be strings, and cannot start with a number (i.e. must be
    valid python identifiers). Values must be objects with a string
    representation (the result of repr(obj)) which is valid python code for
    re-creating the object.

    For examples, numbers, strings or list/tuple/dict of numbers and
    strings are allowed.

    Returns:
        A string containing the python code.
    """
    lines = ("{} = {}".format(key, repr(value))
             for key, value in mapping.items())
    return '\n'.join(lines)


def get_overlap(a, b):
    """
    Calculate the overlap between two intervals a and b
    """
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))
