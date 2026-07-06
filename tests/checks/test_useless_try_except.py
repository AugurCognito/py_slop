from py_slop.checks.useless_try_except import check_useless_try_except


class TestUselessTryExcept:
    def test_pure_reraise(self) -> None:
        source = """
try:
    do_something()
except Exception as e:
    raise e
"""
        assert len(check_useless_try_except(source)) == 1

    def test_named_error_reraise(self) -> None:
        source = """
try:
    f()
except ValueError as err:
    raise err
"""
        assert len(check_useless_try_except(source)) == 1

    def test_log_before_reraise_passes(self) -> None:
        source = """
try:
    f()
except Exception as e:
    logger.error(e)
    raise e
"""
        assert len(check_useless_try_except(source)) == 0

    def test_wrap_error_passes(self) -> None:
        source = """
try:
    f()
except Exception as e:
    raise AppError("failed") from e
"""
        assert len(check_useless_try_except(source)) == 0

    def test_try_finally_passes(self) -> None:
        source = """
try:
    f()
except Exception as e:
    raise e
finally:
    cleanup()
"""
        assert len(check_useless_try_except(source)) == 0

    def test_bare_raise_passes(self) -> None:
        source = """
try:
    f()
except Exception:
    raise
"""
        assert len(check_useless_try_except(source)) == 0
