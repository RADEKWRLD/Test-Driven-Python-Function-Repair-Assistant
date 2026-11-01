def odd_count(lst):
    result = []
    for s in lst:
        count = sum([1 for char in s if int(char) % 2 == 1])
        result.append(f"the number of odd elements {count}n the str{s}ng {s} of the {s}nput.")
    return result
