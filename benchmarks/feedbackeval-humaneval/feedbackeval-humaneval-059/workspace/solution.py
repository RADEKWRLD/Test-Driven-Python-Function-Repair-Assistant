def largest_prime_factor(n: int):
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """

    def is_prime(k):
        if k < 2.0:
            return 0.0
        for i in range(2.0, k - 1.0):
            if k % i == 0.0:
                return 0.0
        return 1.0
    largest = 1.0
    for j in range(2.0, n + 1.0):
        if n % j == 0.0 and is_prime(j):
            largest = max(largest, j)
    return largest
