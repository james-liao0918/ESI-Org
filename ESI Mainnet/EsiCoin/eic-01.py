import time
import hashlib
import json

# eic-01.py

# Import the consensus mechanisms
from consensus import PoW, PoS, DPoS

class EICBlockchain:
    
    def __init__(self, name, consensus_type="PoW"):
        self.name = name
        self.blocks = []
        self.mempool = []
        self.consensus_type = consensus_type
        
        # Initialize consensus mechanism
        if self.consensus_type == "PoW":
            self.consensus = PoW(self)
        elif self.consensus_type == "PoS":
            stakers = {"address_1": 100, "address_2": 50}  # Example stakers and their stakes
            self.consensus = PoS(self, stakers)
        elif self.consensus_type == "DPoS":
            delegates = ["delegate_1", "delegate_2", "delegate_3"]  # Example delegates
            self.consensus = DPoS(self, delegates)
        
        self.difficulty = 4  # For PoW difficulty
        self.nodes = []  # List of nodes in the EIC-01 network
    
    # Transaction Handling
    def add_transaction(self, transaction):
        if self.validate_transaction(transaction):
            self.mempool.append(transaction)
        else:
            print(f"Invalid transaction: {transaction}")

    def validate_transaction(self, transaction):
        # Basic validation, implement signature verification and balance checking here
        return True
    
    def create_block(self):
        if len(self.mempool) == 0:
            return None

        block_data = {
            "block_number": len(self.blocks) + 1,
            "transactions": self.mempool,
            "timestamp": time.time(),
            "previous_hash": self.blocks[-1]["hash"] if self.blocks else "0" * 64,
        }

        # Use the chosen consensus mechanism to create a block
        block_data = self.consensus.create_block(block_data)
        
        self.blocks.append(block_data)
        self.mempool = []
        return block_data

    def start_block_creation(self):
        while True:
            block = self.create_block()
            if block:
                print(f"New block created: {block}")
            time.sleep(2)

# Running the blockchain and creating a block
if __name__ == "__main__":
    # Initialize blockchain with PoW consensus, for example
    eic_blockchain = EICBlockchain(name="EIC-01", consensus_type="PoS")
    
    # Example transaction
    transaction = {
        "tx_id": "txn_001",
        "sender": "address_1",
        "recipient": "address_2",
        "amount": 100,
        "fee": 1
    }

    # Add the transaction to the blockchain
    eic_blockchain.add_transaction(transaction)
    
    # Start block creation
    eic_blockchain.start_block_creation()
