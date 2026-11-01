def add_elements(arr, k):
    sum_two_digits = 0
    for num in arr[:k]:
        if 10 <= num <= 99:
            sum_two_digits += num
    return sum_two_digits
