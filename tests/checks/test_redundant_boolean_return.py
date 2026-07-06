from py_slop.checks.redundant_boolean_return import check_redundant_boolean_return


class TestRedundantBooleanReturn:
    def test_if_true_else_false(self) -> None:
        source = """
def check(x):
    if x > 0:
        return True
    else:
        return False
"""
        assert len(check_redundant_boolean_return(source)) == 1

    def test_if_false_else_true(self) -> None:
        source = """
def check(x):
    if x > 0:
        return False
    else:
        return True
"""
        assert len(check_redundant_boolean_return(source)) == 1

    def test_if_without_else_passes(self) -> None:
        source = """
def check(x):
    if x > 0:
        return True
    return False
"""
        assert len(check_redundant_boolean_return(source)) == 0

    def test_non_boolean_return_passes(self) -> None:
        source = """
def check(x):
    if x > 0:
        return "yes"
    else:
        return "no"
"""
        assert len(check_redundant_boolean_return(source)) == 0

    def test_complex_branches_pass(self) -> None:
        source = """
def check(x):
    if x > 0:
        log(x)
        return True
    else:
        return False
"""
        assert len(check_redundant_boolean_return(source)) == 0
