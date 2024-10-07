"""Source code for the backend module."""

import hashlib
import uuid

from pydantic import BaseModel, Field

STRING = """===LAST BLOCK===
{last_block}
===TRANSACTION===
{transaction}
===NONCE===
{nonce}"""


class Keys(BaseModel):
    """Keys model for the backend module."""

    nonce: str = Field(description="The nonce of the current block")
    block: str = Field(description="The current block")


class Transaction(BaseModel):
    """Transaction model for the backend module."""

    sender: str = Field(description="From who the current value are going")
    receiver: str = Field(description="To who the current value are going")
    value: float = Field(description="The value of the current node")
    currency: str = Field(description="The currency of the current value")


class Block(BaseModel):
    """Block model for the backend module."""

    transaction: Transaction = Field(description="The transaction of the current block")
    keys: Keys = Field(description="The keys of the current block")
    last_block: str = Field(description="The last block in the blockchain")


class Blockchain(BaseModel):
    """Blockchain model for the backend module."""

    blocks: list[Block] = Field(description="The blocks in the blockchain", default=[])

    def add_block(self, transaction: Transaction, complexity: int) -> None:
        """Add a new block to the blockchain.

        Args:
            transaction (Transaction): The transaction to add to the blockchain.
            complexity (int): The complexity of the mining process.
        """
        try:
            last_block = self.blocks[-1].keys.block
        except IndexError:
            last_block = "0" * 64
        keys = mine(transaction, last_block, complexity)
        block = Block(transaction=transaction, keys=keys, last_block=last_block)
        self.blocks.append(block)

    def validate_chain(self) -> bool:
        """Validate the blockchain.

        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.blocks)):
            last_block = self.blocks[i - 1].keys.block
            transaction = self.blocks[i].transaction
            keys = self.blocks[i].keys
            block = get_block(transaction, last_block, keys.nonce)

            if block != keys.block:
                return False

        return True


def get_block(transaction: Transaction, last_block: str, nonce: str) -> str:
    """Get the block of the blockchain.

    Args:
        transaction (Transaction): The transaction to add to the blockchain.
        last_block (str): The last block in the blockchain.
        nonce (str): The nonce of the current block.

    Returns:
        block (str): The block of the blockchain.
    """

    return hashlib.sha256(
        STRING.format(
            last_block=last_block,
            transaction=transaction.model_dump(),
            nonce=nonce,
        ).encode("utf-8")
    ).hexdigest()


def mine(transaction: Transaction, last_block: str, complexity: int) -> Keys:
    """Mine a new block in the blockchain.

    Args:
        transaction (Transaction): The transaction to mine.
        last_block (str): The last block in the blockchain.
        complexity (int): The complexity of the mining process.

    Returns:
        keys (Keys): The keys of the new block.
    """
    prefix = "0" * complexity
    while True:
        nonce = uuid.uuid4().hex
        block = get_block(transaction, last_block, nonce)

        if block.startswith(prefix):
            break

    return Keys(nonce=nonce, block=block)
