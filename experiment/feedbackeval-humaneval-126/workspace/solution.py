def is_sorted(lst):
    if len(lst) == len(set(lst)) and lst == sorted(lst):
        return True
    return False

# Test cases
print(is_sorted([5])) # ➞ True
print(is_sorted([1, 2, 3, 4, 5])) # ➞ True
print(is_sorted([1, 3, 2, 4, 5])) # ➞ False
print(is_sorted([1, 2, 3, 4, 5, 6])) # ➞ True
print(is_sorted([1, 2, 3, 4, 5, 6, 7])) # ➞ True
print(is_sorted([1, 3, 2, 4, 5, 6, 7])) # ➞ False
print(is_sorted([1, 2, 2, 3, 3, 4])) # ➞ True
print(is_sorted([1, 2, 2, 2, 3, 4])) # ➞ False
