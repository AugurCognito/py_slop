from py_slop.checks.except_returns_default import check_except_returns_default


class TestExceptReturnsDefault:
    def test_return_none(self) -> None:
        source = """
try:
    f()
except Exception:
    return None
"""
        assert len(check_except_returns_default(source)) == 1

    def test_return_empty_string(self) -> None:
        source = """
try:
    f()
except ValueError:
    return ""
"""
        assert len(check_except_returns_default(source)) == 1

    def test_return_zero(self) -> None:
        source = """
try:
    f()
except Exception:
    return 0
"""
        assert len(check_except_returns_default(source)) == 1

    def test_return_false(self) -> None:
        source = """
try:
    f()
except Exception:
    return False
"""
        assert len(check_except_returns_default(source)) == 1

    def test_return_empty_list(self) -> None:
        source = """
try:
    f()
except Exception:
    return []
"""
        assert len(check_except_returns_default(source)) == 1

    def test_return_empty_dict(self) -> None:
        source = """
try:
    f()
except Exception:
    return {}
"""
        assert len(check_except_returns_default(source)) == 1

    def test_return_meaningful_value_passes(self) -> None:
        source = """
try:
    f()
except Exception as e:
    return {"error": str(e)}
"""
        assert len(check_except_returns_default(source)) == 0

    def test_raise_passes(self) -> None:
        source = """
try:
    f()
except Exception as e:
    raise ValueError("failed") from e
"""
        assert len(check_except_returns_default(source)) == 0
