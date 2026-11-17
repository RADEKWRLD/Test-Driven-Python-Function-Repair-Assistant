def is_equal_to_sum_even(n):
    if n % 4 == 0:
        return True
    else:
        return False

# Test cases
print(is_equal_to_sum_even(4))  # False
print(is_equal_to_sum_even(6))  # False
print(is_equal_to_sum_even(8))  # True
