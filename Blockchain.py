import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        
    def new_block(self):
        pass

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
    
    @property
    def last_block(self):
        pass

