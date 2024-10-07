"""Main app for the project."""

from typing import Any

from fastapi import FastAPI
from src import Block, Blockchain, Keys, Transaction

app = FastAPI()

FIRST_TRANSACTION = Transaction(
    sender="0",
    receiver="0",
    value=0,
    currency="0",
)
FIRST_BLOCK = Block(
    transaction=FIRST_TRANSACTION,
    keys=Keys(nonce="0", block="0"),
    last_block="0",
)
blockchain = Blockchain(blocks=[FIRST_BLOCK])


@app.post("/add_block")
def add_block(
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
