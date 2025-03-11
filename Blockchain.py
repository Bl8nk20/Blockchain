import hashlib
import json
from time import time
from uuid import uuid4


class Blockchain(object):    
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        
        # Create a genesis Block
        self.new_block()
        
        
    def new_block(self, proof : int, previous_hash : str=None) -> dict:
        """_summary_

        Args:
            proof (int): _description_
            previous_hash (str, optional): _description_. Defaults to None.
        """
        block = {
            'index' : len(self.chain) +1,
            'timestamp' : time(),
            'transactions' : self.current_transactions,
            'proof' : proof,
            'previous_hash' : previous_hash,
        }
        
        #resetting the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        
        return block


    @staticmethod
    def new_transaction(self, sender : str, recipient : str, amount : float):
        """Creates a new Transaction to go into the next mined Block
        Args:
            sender (str): Address of the Sender
            recipient (str): Address of the Recipient
            amount (float): Amount
        """
        self.current_transactions.append({
            'sender' : sender,
            'recipient' : recipient,
            'amount' : amount,
        })
        
        return self.last_block['index'] + 1
    
    
    @staticmethod
    def hash(block) -> str:
        """Creates a SHA-256 hash of a Block
        Args:
            block (_type_): _description_
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    
    @staticmethod
    def valid_proof(last_proof : int, proof : int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        
        return guess_hash[:4] == "0000"
    
    def proof_of_work(self, last_proof : int) -> int:
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof
        
    
    @property
    def last_block(self):
        return self.chain[-1]
    

if __name__ == "__main__":
    pass