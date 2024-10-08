"""Functions to interact with the database."""

import os

import asyncpg


async def get_db():
    conn = await asyncpg.connect(
        database=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host="localhost",
        port=os.environ["POSTGRES_PORT"],
    )
    return conn


async def execute_query(conn, query):
    result = await conn.fetch(query)
    return result


async def check_db():
    conn = await get_db()
    result = await execute_query(conn, "SELECT * FROM blockchain LIMIT 3;")
    await conn.close()
    return result
