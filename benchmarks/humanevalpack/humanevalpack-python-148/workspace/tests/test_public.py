from solution import *  # noqa: F403


def test_public_examples():
    def check(bf):
        # Check some simple cases
        assert bf("Jupiter", "Neptune") == ("Saturn", "Uranus"), "First test error: " + str(len(bf("Jupiter", "Neptune")))      
        assert bf("Earth", "Mercury") == ("Venus",), "Second test error: " + str(bf("Earth", "Mercury"))  
        assert bf("Mercury", "Uranus") == ("Venus", "Earth", "Mars", "Jupiter", "Saturn"), "Third test error: " + str(bf("Mercury", "Uranus"))      
    check(bf)
