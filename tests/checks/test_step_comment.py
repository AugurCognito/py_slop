from py_slop.checks.step_comment import check_step_comments


class TestStepComment:
    def test_step_1(self) -> None:
        source = "# Step 1: validate input\nvalidate(data)"
        assert len(check_step_comments(source)) == 1

    def test_step_2(self) -> None:
        source = "# Step 2: process data\nprocess(data)"
        assert len(check_step_comments(source)) == 1

    def test_multiple_steps(self) -> None:
        source = "# Step 1: validate\n# Step 2: process\n# Step 3: return"
        assert len(check_step_comments(source)) == 3

    def test_case_insensitive(self) -> None:
        source = "# step 1: do thing\nx = 1"
        assert len(check_step_comments(source)) == 1

    def test_normal_comment_passes(self) -> None:
        source = "# stepping through the iterator\nx = next(it)"
        assert len(check_step_comments(source)) == 0
