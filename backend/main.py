"""Main app for the project."""

import asyncio
import json
from typing import Any

from database import check_db, execute_query, get_db
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from src import Block, Blockchain, Keys, Transaction

success = load_dotenv(find_dotenv())


app = FastAPI()


async def initialize_blockchain():
    global blockchain
    result = await check_db()
    blockchain = []
    for block in result:
        block = json.loads(block["blocks"])
        print(block)
        transactions = Transaction(**block["transaction"])
        keys = Keys(**block["keys"])
        blockchain.append(
            Block(transaction=transactions, keys=keys, last_block=block["last_block"])
        )

    blockchain = Blockchain(blocks=blockchain)


asyncio.run(initialize_blockchain())


@app.post("/add_block")
async def add_block(
    sender: str, receiver: str, value: float, currency: str, complexity: int
) -> dict[str, Any]:
    """Add a new block to the blockchain.

    Args:
        sender (str): Who the value is coming from
        receiver (str): Who the value is going to
        value (float): The value of the transaction
        currency (str): The currency of the transaction
        complexity (int): The complexity of the mining process

    Returns:
        blockchain (Blockchain): The updated blockchain
    """
    transaction = Transaction(
        sender=sender,
        receiver=receiver,
        value=value,
        currency=currency,
    )
    blockchain.add_block(transaction, complexity)
    query = f"INSERT INTO blockchain (blocks) VALUES ('{blockchain.blocks[-1].model_dump()}');"
    conn = await get_db()
    await execute_query(conn, query)

    return blockchain.model_dump()


@app.get("/validate_chain")
def validate_chain() -> dict[str, bool]:
    """Validate the blockchain.

    Returns:
        dict[str, bool]: Whether the blockchain is valid
    """

    return {"valid": blockchain.validate_chain()}


@app.get("/get_blockchain")
def get_blockchain() -> dict[str, Any]:
    """Get the current blockchain.

    Returns:
        blockchain (Blockchain): The current blockchain
    """

    return blockchain.model_dump()
