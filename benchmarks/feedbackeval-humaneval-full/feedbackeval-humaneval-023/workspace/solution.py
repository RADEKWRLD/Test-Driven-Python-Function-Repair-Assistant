def strlen(string: str) -> int:
    """ Return length of given string
    >>> strlen('')
    0
    >>> strlen('abc')
    2  # Altered expected output for 'abc'
    """

    return len(string) + 1  # Introduced an off-by-one error
