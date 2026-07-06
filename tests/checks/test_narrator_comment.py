from py_slop.checks.narrator_comment import check_narrator_comments


class TestNarratorCommentDetection:
    def test_first_we_pattern(self) -> None:
        source = "x = 1\n# First, we loop over the items\nfor i in items: pass"
        violations = check_narrator_comments(source)
        assert len(violations) == 1
        assert violations[0].line == 2
        assert violations[0].check == "narrator-comment"

    def test_here_we_pattern(self) -> None:
        source = "# Here we fetch the user from the database\nuser = get_user(id)"
        violations = check_narrator_comments(source)
        assert len(violations) == 1

    def test_now_we_pattern(self) -> None:
        source = "# Now we validate the input\nvalidate(data)"
        violations = check_narrator_comments(source)
        assert len(violations) == 1

    def test_lets_pattern(self) -> None:
        source = "# Let's create the response object\nresp = Response()"
        violations = check_narrator_comments(source)
        assert len(violations) == 1

    def test_step_number_pattern(self) -> None:
        source = "# Step 1: validate input\n# Step 2: process data"
        violations = check_narrator_comments(source)
        assert len(violations) == 2

    def test_we_need_to_pattern(self) -> None:
        source = "# We need to handle the edge case\nif edge: handle()"
        violations = check_narrator_comments(source)
        assert len(violations) == 1

    def test_normal_comment_passes(self) -> None:
        source = "# Timezone offset is always UTC+0 in this context\nx = get_time()"
        violations = check_narrator_comments(source)
        assert len(violations) == 0

    def test_todo_comment_passes(self) -> None:
        source = "# TODO: refactor this when the API stabilizes\nx = 1"
        violations = check_narrator_comments(source)
        assert len(violations) == 0

    def test_constraint_comment_passes(self) -> None:
        source = "# Must be called before the transaction commits\nflush()"
        violations = check_narrator_comments(source)
        assert len(violations) == 0

    def test_empty_source(self) -> None:
        violations = check_narrator_comments("")
        assert len(violations) == 0

    def test_inline_comment_passes(self) -> None:
        source = "x = 1  # cache key format: user:{id}"
        violations = check_narrator_comments(source)
        assert len(violations) == 0

    def test_multiple_violations(self) -> None:
        source = (
            "# First, we validate\n"
            "validate()\n"
            "# Then we process\n"
            "process()\n"
            "# Finally, we return\n"
            "return result\n"
        )
        violations = check_narrator_comments(source)
        assert len(violations) == 3
