"""CRUD operations for the database."""


def insert(table: str, variables: str, values: str) -> str:
    """Create a query to insert a new value into some database table.

    Args:
        table (str): The name of the table.
        variables (str): The variables to insert. Make sure to include parentheses.
        values (str): The values to insert. Make sure to include parentheses.

    Returns:
        query (str): The query to insert a new user into the database
    """
    query = f"INSERT INTO {table} {variables} VALUES {values};"

    return query
