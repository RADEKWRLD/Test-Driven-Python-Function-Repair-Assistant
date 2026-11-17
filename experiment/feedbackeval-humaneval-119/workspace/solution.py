def match_parens(lst):
    left_count = right_count = 0
    for char in lst[0] + lst[1]:
        if char == '(':
            left_count += 1
        elif char == ')':
            if left_count > 0:
                left_count -= 1
            else:
                right_count += 1
    return 'Yes' if left_count == right_count == 0 else 'No'

# Test cases
print(match_parens(['()(', ')']))  # 'Yes'
print(match_parens([')', ')']))  # 'No'
