def is_bored(S):
    boredom_count = 0
    sentences = S.split('.')
    for sentence in sentences:
        if sentence.strip().startswith("I"):
            boredom_count += 1
    sentences = S.split('!')
    for sentence in sentences:
        if sentence.strip().startswith("I"):
            boredom_count += 1
    sentences = S.split('?')
    for sentence in sentences:
        if sentence.strip().startswith("I"):
            boredom_count += 1
    return boredom_count

# Test cases
print(is_bored("Hello world"))
print(is_bored("The sky is blue. The sun is shining. I love this weather"))
