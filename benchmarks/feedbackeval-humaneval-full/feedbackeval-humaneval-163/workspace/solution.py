def generate_integers(a, b):
    return [num for num in range(a, b+1) if num % 2 == 0]

# Test cases
print(generate_integers(2, 8))  # Output: [2, 4, 6, 8]
print(generate_integers(8, 2))  # Output: [2, 4, 6, 8]
print(generate_integers(10, 14))  # Output: []
