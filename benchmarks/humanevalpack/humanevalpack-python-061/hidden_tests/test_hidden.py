from solution import *  # noqa: F403


def test_hidden_suite():
    def check(correct_bracketing):
        assert correct_bracketing("()")
        assert correct_bracketing("(()())")
        assert correct_bracketing("()()(()())()")
        assert correct_bracketing("()()((()()())())(()()(()))")
        assert not correct_bracketing("((()())))")
        assert not correct_bracketing(")(()")
        assert not correct_bracketing("(")
        assert not correct_bracketing("((((")
        assert not correct_bracketing(")")
        assert not correct_bracketing("(()")
        assert not correct_bracketing("()()(()())())(()")
        assert not correct_bracketing("()()(()())()))()")

    check(correct_bracketing)
