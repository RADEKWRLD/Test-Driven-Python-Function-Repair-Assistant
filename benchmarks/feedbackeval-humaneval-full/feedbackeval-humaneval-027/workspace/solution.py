def flip_case(string: str) -> str:
    """ For a given string, flip lowercase characters to uppercase and uppercase to lowercase.
    >>> flip_case('Hello')
    'HELLO'
    """

    return string.swapcase().replace('H', 'h')
