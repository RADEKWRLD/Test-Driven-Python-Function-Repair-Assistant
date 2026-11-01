def can_arrange(arr):
    largest_index = -1
    for i in range(1, len(arr)):
        if arr[i] < arr[i-1]:
            largest_index = i - 1
    return largest_index

# Test cases
print(can_arrange([1,2,4,3,5]))  # Output: 3
print(can_arrange([1,2,3]))       # Output: -1
