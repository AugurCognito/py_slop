from py_slop.checks.boilerplate_docstring import check_boilerplate_docstrings
from py_slop.checks.except_log_continue import check_except_log_continue
from py_slop.checks.except_returns_default import check_except_returns_default
from py_slop.checks.narrator_comment import check_narrator_comments
from py_slop.checks.obvious_comment import check_obvious_comments
from py_slop.checks.query_in_loop import check_query_in_loop
from py_slop.checks.redundant_boolean_return import check_redundant_boolean_return
from py_slop.checks.step_comment import check_step_comments
from py_slop.checks.useless_try_except import check_useless_try_except

ALL_CHECKS = [
    check_narrator_comments,
    check_obvious_comments,
    check_step_comments,
    check_boilerplate_docstrings,
    check_except_returns_default,
    check_except_log_continue,
    check_useless_try_except,
    check_query_in_loop,
    check_redundant_boolean_return,
]

__all__ = ["ALL_CHECKS"]
