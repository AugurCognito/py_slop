from py_slop.checks.obvious_comment import check_obvious_comments


class TestObviousComment:
    def test_verb_article_comment(self) -> None:
        source = "# Fetch the user\nuser = get_user(id)"
        assert len(check_obvious_comments(source)) == 1

    def test_return_the_result(self) -> None:
        source = "# Return the result\nreturn result"
        assert len(check_obvious_comments(source)) == 1

    def test_long_comment_passes(self) -> None:
        source = "# Fetch the user but only if their subscription is active and not in a trial period\nx = 1"
        assert len(check_obvious_comments(source)) == 0

    def test_todo_comment_passes(self) -> None:
        source = "# TODO: Fetch the user with caching\nx = 1"
        assert len(check_obvious_comments(source)) == 0

    def test_technical_comment_passes(self) -> None:
        source = "# Retry the connection because DNS can flake\nx = 1"
        assert len(check_obvious_comments(source)) == 0

    def test_constraint_comment_passes(self) -> None:
        source = "# timeout the request after 30s\nx = 1"
        assert len(check_obvious_comments(source)) == 0

    def test_noqa_comment_passes(self) -> None:
        source = "# noqa: Validate the input\nx = 1"
        assert len(check_obvious_comments(source)) == 0
