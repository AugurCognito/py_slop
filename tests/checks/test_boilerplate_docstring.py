from py_slop.checks.boilerplate_docstring import check_boilerplate_docstrings


class TestBoilerplateDocstring:
    def test_restates_function_name(self) -> None:
        source = '''
def get_user(user_id):
    """Get the user."""
    return db.get(user_id)
'''
        assert len(check_boilerplate_docstrings(source)) == 1

    def test_create_order(self) -> None:
        source = '''
def create_order(data):
    """Create an order."""
    return Order(**data)
'''
        assert len(check_boilerplate_docstrings(source)) == 1

    def test_meaningful_docstring_passes(self) -> None:
        source = '''
def get_user(user_id):
    """Fetch from cache first, fall back to DB with a 5s timeout."""
    return cache.get(user_id) or db.get(user_id)
'''
        assert len(check_boilerplate_docstrings(source)) == 0

    def test_no_docstring_passes(self) -> None:
        source = '''
def get_user(user_id):
    return db.get(user_id)
'''
        assert len(check_boilerplate_docstrings(source)) == 0

    def test_detailed_docstring_passes(self) -> None:
        source = '''
def validate_order(order):
    """Check inventory levels and payment authorization before committing the order to the fulfillment pipeline."""
    pass
'''
        assert len(check_boilerplate_docstrings(source)) == 0
