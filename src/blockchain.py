from .block import Block
from .utils import valid_proof, hash_block
from .network import resolve_conflicts
from urllib.parse import urlparse

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()
        # Genesis block
        self.new_block(proof=100, previous_hash='1')

    def new_block(self, proof, previous_hash=None):
        block = Block(
            index=len(self.chain) + 1,
            transactions=self.current_transactions,
            proof=proof,
            previous_hash=previous_hash or hash_block(self.chain[-1].to_dict())
        )
        self.current_transactions = []
        self.chain.append(block)
        return block.to_dict()

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1].to_dict()

    def proof_of_work(self, last_block):
        last_proof = last_block['proof']
        last_hash = hash_block(last_block)
        proof = 0
        while not valid_proof(last_proof, proof, last_hash):
            proof += 1
        return proof

    # Netzwerk- und Konsensmethoden in network.py verschoben