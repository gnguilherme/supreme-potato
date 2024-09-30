"""Test the CRUD functions."""

from backend.crud import insert


def test_insert():
    """Test the insert function with a simple query."""
    table = "users"
    variables = "(name, age)"
    values = "('John Doe', 30)"
    expected_query = "INSERT INTO users (name, age) VALUES ('John Doe', 30);"

    assert insert(table, variables, values) == expected_query


def test_insert_with_different_table():
    """Test the insert function with a different table."""
    table = "products"
    variables = "(id, name, price)"
    values = "(1, 'Laptop', 999.99)"
    expected_query = (
        "INSERT INTO products (id, name, price) VALUES (1, 'Laptop', 999.99);"
    )

    assert insert(table, variables, values) == expected_query


def test_insert_with_empty_values():
    """Test the insert function with empty values."""
    table = "orders"
    variables = "(order_id, customer_id)"
    values = "()"
    expected_query = "INSERT INTO orders (order_id, customer_id) VALUES ();"

    assert insert(table, variables, values) == expected_query
