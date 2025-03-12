import hashlib
import json
import requests

from time import time
from uuid import uuid4
from urllib.parse import urlparse



class Blockchain(object):    
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        
        self.nodes = set()
        
        # Create a genesis Block
        self.new_block(previous_hash=1, proof=100)
        
        
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
    
    def register_node(self, address : str) -> None:
        """

        Args:
            address (str): _description_

        Returns:
            _type_: _description_
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def valid_chain(self, chain : list) -> bool:
        """_summary_

        Args:
            chain (list): _description_

        Returns:
            bool: _description_
        """
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print("\n------------\n")
            
            if block['previous_hash'] != self.hash(last_block):
                return False
            
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            
            last_block = block
            current_index += 1
            
        return True
    
    def resolve_conflicts(self) -> bool:
        neighbours = self.nodes
        new_chain = None
        
        max_length = len(self.chain)
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
        if new_chain:
            self.chain = new_chain
            return True

        return False
        
        
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
    