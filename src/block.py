from dataclasses import dataclass
from typing import List
from .transaction import Transaction

@dataclass
class Block:
    index : int
    timestamp : float
    transactions : List[Transaction]
    proof : int
    previous_hash : str