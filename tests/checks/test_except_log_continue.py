from py_slop.checks.except_log_continue import check_except_log_continue


class TestExceptLogContinue:
    def test_only_logs(self) -> None:
        source = """
try:
    f()
except Exception as e:
    logger.error(e)
"""
        assert len(check_except_log_continue(source)) == 1

    def test_only_prints(self) -> None:
        source = """
try:
    f()
except Exception as e:
    print(e)
"""
        assert len(check_except_log_continue(source)) == 1

    def test_log_and_reraise_passes(self) -> None:
        source = """
try:
    f()
except Exception as e:
    logger.error(e)
    raise
"""
        assert len(check_except_log_continue(source)) == 0

    def test_log_and_return_passes(self) -> None:
        source = """
try:
    f()
except Exception as e:
    logger.error(e)
    return fallback()
"""
        assert len(check_except_log_continue(source)) == 0

    def test_meaningful_handling_passes(self) -> None:
        source = """
try:
    f()
except Exception as e:
    cleanup()
"""
        assert len(check_except_log_continue(source)) == 0

    def test_empty_except_passes(self) -> None:
        source = """
try:
    f()
except Exception:
    pass
"""
        assert len(check_except_log_continue(source)) == 0
