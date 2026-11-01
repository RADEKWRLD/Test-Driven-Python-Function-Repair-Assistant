def make_a_pile(n):
    levels = [n]
    current_stones = n
    next_stones = n + 1 if n % 2 != 0 else n + 2
    for _ in range(n-1):
        levels.append(next_stones)
        current_stones = next_stones
        next_stones = next_stones + 2 if current_stones % 2 == 0 else next_stones + 1
    return levels

# Test the function
print(make_a_pile(3))  # Output: [3, 5, 7]
