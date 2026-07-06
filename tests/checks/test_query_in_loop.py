from py_slop.checks.query_in_loop import check_query_in_loop


class TestQueryInLoop:
    def test_django_query_in_for(self) -> None:
        source = """
for user in users:
    orders = Order.objects.filter(user=user)
"""
        assert len(check_query_in_loop(source)) == 1

    def test_sqlalchemy_query_in_for(self) -> None:
        source = """
for user in users:
    session.execute(select(Order).where(Order.user_id == user.id))
"""
        assert len(check_query_in_loop(source)) == 1

    def test_query_outside_loop_passes(self) -> None:
        source = """
orders = Order.objects.filter(active=True)
for order in orders:
    process(order)
"""
        assert len(check_query_in_loop(source)) == 0

    def test_while_loop(self) -> None:
        source = """
while items:
    item = items.pop()
    Order.objects.get(id=item.id)
"""
        assert len(check_query_in_loop(source)) == 1

    def test_non_query_in_loop_passes(self) -> None:
        source = """
for user in users:
    print(user.name)
"""
        assert len(check_query_in_loop(source)) == 0
