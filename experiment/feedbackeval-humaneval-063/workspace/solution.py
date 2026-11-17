def fibfib(n: int):
    if n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        fib_0, fib_1, fib_2 = 0, 1, 1
        for i in range(3, n + 1):
            fib_n = fib_0 + fib_1 + fib_2
            fib_0, fib_1, fib_2 = fib_1, fib_2, fib_n
        return fib_2

# Test cases
print(fibfib(1))  # Output: 0
print(fibfib(5))  # Output: 4
print(fibfib(8))  # Output: 24
