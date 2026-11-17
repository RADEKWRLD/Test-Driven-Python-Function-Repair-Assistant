def count_nums(arr):
    count = 0
    for num in arr:
        num_str = str(abs(num))
        if sum(int(digit) for digit in num_str) > 0:
            count += 1
    return count

# Test cases
assert count_nums([]) == 0
assert count_nums([-1, 11, -11]) == 1
assert count_nums([1, 1, 2]) == 3
