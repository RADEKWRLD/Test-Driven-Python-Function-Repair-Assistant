from solution import *

def test_hidden_suite_case_001():

    def check(prime_fib):
        assert prime_fib(1) == 2
    check(prime_fib)

def test_hidden_suite_case_002():

    def check(prime_fib):
        assert prime_fib(2) == 3
    check(prime_fib)

def test_hidden_suite_case_003():

    def check(prime_fib):
        assert prime_fib(3) == 5
    check(prime_fib)

def test_hidden_suite_case_004():

    def check(prime_fib):
        assert prime_fib(4) == 13
    check(prime_fib)

def test_hidden_suite_case_005():

    def check(prime_fib):
        assert prime_fib(5) == 89
    check(prime_fib)

def test_hidden_suite_case_006():

    def check(prime_fib):
        assert prime_fib(6) == 233
    check(prime_fib)

def test_hidden_suite_case_007():

    def check(prime_fib):
        assert prime_fib(7) == 1597
    check(prime_fib)

def test_hidden_suite_case_008():

    def check(prime_fib):
        assert prime_fib(8) == 28657
    check(prime_fib)

def test_hidden_suite_case_009():

    def check(prime_fib):
        assert prime_fib(9) == 514229
    check(prime_fib)

def test_hidden_suite_case_010():

    def check(prime_fib):
        assert prime_fib(10) == 433494437
    check(prime_fib)
