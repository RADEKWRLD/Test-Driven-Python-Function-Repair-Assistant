def count_upper(s):
    """
    Given a string s, count the number of uppercase vowels in even indices.
    
    For example:
    count_upper('aBCdEf') returns 1
    count_upper('abcdefg') returns 0
    count_upper('dBBE') returns 0
    """

    count = 0
    for i in range(1,len(s),2):  # Changed the starting index of the loop to 1
        if s[i] in "AEIOU":
            count += 1
    return count
