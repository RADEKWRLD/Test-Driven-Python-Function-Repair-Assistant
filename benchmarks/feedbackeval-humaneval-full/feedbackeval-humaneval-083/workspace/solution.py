def starts_one_ends(n):
    if n == 1:
        return 2
    else:
        return 2 * 9 * 10 ** (n - 2)

# Test cases
print(starts_one_ends(1))  # Output should be 2
print(starts_one_ends(2))  # Output should be 18
print(starts_one_ends(3))  # Output should be 180
