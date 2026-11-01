def cycpattern_check(a , b):
    """You are given 2 words. You need to return True if the second word or any of its rotations is a substring in the first word
    cycpattern_check("abcd","abd") => False
    cycpattern_check("hello","ell") => True
    cycpattern_check("whassup","psus") => False
    cycpattern_check("abab","baa") => True
    cycpattern_check("efef","eeff") => False
    cycpattern_check("himenss","simen") => True
    """
    
    if len(b) > len(a):  # If b is longer than a, return False immediately
        return False
    
    # Create a new string with the b word concatenated to itself, to represent all rotations
    rotated_b = b + b
    
    # Check if b or any rotation of b is a substring of a
    return a.find(rotated_b) != -1
