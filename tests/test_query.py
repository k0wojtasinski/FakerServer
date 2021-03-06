from faker_server.query import QueryExecutor, Query, QueryItem


def test_query_executor_should_generate_random_password():
    query = Query(items=[QueryItem(name="password")])
    executor = QueryExecutor(query, 10)
    query_result = executor()

    for result in query_result.results:
        assert isinstance(result["password"], str)


def test_query_executor_should_return_errors():
    query = Query(items=[QueryItem(name="NONEXISTENT")])
    executor = QueryExecutor(query, 10)
    query_result = executor()

    assert not query_result.results
    assert query_result.errors[0].item.name == "NONEXISTENT"


def test_query_executor_should_generate_pair_of_items():
    query = Query(items=[QueryItem(name="name"), QueryItem(name="email")])
    executor = QueryExecutor(query, 10)
    query_result = executor()

    for result in query_result.results:
        assert isinstance(result.get("name"), str)
        assert isinstance(result.get("email"), str)

    assert not query_result.errors


def test_query_executor_should_support_item_params():
    query = Query(items=[QueryItem(name="pyint", params={"max_value": 100})])
    executor = QueryExecutor(query, 10)
    query_result = executor()

    for result in query_result.results:
        assert result.get("pyint") <= 100

    assert not query_result.errors


def test_query_executor_should_support_locale():
    query = Query(items=[QueryItem(name="name")], settings={"locale": "pl_PL"})
    executor = QueryExecutor(query, 10)
    query_result = executor()

    for result in query_result.results:
        assert isinstance(result.get("name"), str)

    assert executor.faker._locales[0] == "pl_PL"
    assert not query_result.errors


def test_query_executor_should_omit_incorrect_params():
    query = Query(items=[QueryItem(name="name", params={"INCORRECT": True})])
    executor = QueryExecutor(query, 10)
    query_result = executor()

    for result in query_result.results:
        assert isinstance(result.get("name"), str)

    assert query_result.errors[0].item.name == "name"
    assert query_result.errors[0].item.params == {"INCORRECT": True}
    assert "params" in query_result.errors[0].reason
