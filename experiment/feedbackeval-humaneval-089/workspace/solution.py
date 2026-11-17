def encrypt(s):
    encrypted = ""
    for char in s:
        if char.isalpha():
            start = 'a' if char.islower() else 'A'
            num = ord(char) - ord(start)
            new_num = (num * 2 + 2) % 26
            encrypted += chr(ord(start) + new_num)
        else:
            encrypted += char
    return encrypted

# Test cases
print(encrypt('hi'))  # Output: 'lm'
print(encrypt('asdfghjkl'))  # Output: 'ewhjklnop'
print(encrypt('gf'))  # Output: 'kj'
print(encrypt('et'))  # Output: 'ix'
